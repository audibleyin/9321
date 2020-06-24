from flask import Flask
from flask_restplus import Resource, Api, fields
import requests
import sqlite3
import os
import time
import re

app = Flask(__name__)
api = Api(app, title="World Bank Economic Indicators", description=" by Chen Wu z5244467")


# database control, for executing SQL command and fetching results
def control_db(database, command):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    if command.count(';') > 1:
        cursor.executescript(command)
    else:
        cursor.execute(command)
    result = cursor.fetchall()  # If multiple commands, no output will be fetched
    connection.commit()
    connection.close()
    return result


# database initialization
def create_db(db_file):
    if os.path.exists(db_file):
        print('Database already exists.')
        return False
    print('Creating database ...')
    control_db(db_file,
               'CREATE TABLE Collection('
               'collection_id INTEGER UNIQUE NOT NULL,'
               'collection_name VARCHAR(100),'
               'indicator VARCHAR(100),'
               'indicator_value VARCHAR(100),'
               'creation_time DATE,'
               'CONSTRAINT collection_pkey PRIMARY KEY (collection_id));'
               +
               'CREATE TABLE entries('
               'id INTEGER NOT NULL,'
               'country VARCHAR(100),'
               'date VARCHAR(10),'
               'value VARCHAR(100),'
               'CONSTRAINT entries_fkey FOREIGN KEY (id) REFERENCES Collection(collection_id));'
               )
    return True


# remote API request, fetching data from worldbank API
def urlrequest(indicator, page):
    response = requests.get(
        "http://api.worldbank.org/v2/countries/all/indicators/{}?date=2012:2017&format=json&per_page=500&page={}".format(
            indicator, page))
    if len(response.json()) > 1:
        data = response.json()[1]
        return data

# convert SQL query result to json-like format, format 4
def retrieve_json1(col_query, entries_query):
    result = {"id": int(col_query[0][0]),
              "indicator": col_query[0][2],
              "indicator_value": col_query[0][3],
              "creation_time": col_query[0][4],
              "entries": list()
              }
    for i in range(len(entries_query)):
        if entries_query[i][2] != "null":
            result["entries"].append({"country": entries_query[i][0],
                                      "value": eval(entries_query[i][2])
                                      })
    return result


# uniform request handler, all requests received will be firstly handled by this function
def handlerequestq6(database, collection, **kwargs):
    up_test = re.search("^(top)(\\d+)$", kwargs['query'])
    down_test = re.search("^(bottom)(\\d+)$", kwargs['query'])
    if up_test:
        return handleget(database, collection, 'get_up_down', collection_id=kwargs['collection_id'],
                         year=kwargs['year'], flag='top', value=up_test.group(2))
    if down_test:
        return handleget(database, collection, 'get_up_down', collection_id=kwargs['collection_id'],
                         year=kwargs['year'], flag='bottom', value=down_test.group(2))
    else:
        api.abort(400, "Your input arguments are not in correct format! Must be either top<int> or bottom<int>.")


# dealing with all get requests, for question 3-6
def handleget(database, collection, operation, **kwargs):
    # question 3, get all collections
    if operation == 'getALLid':
        query = control_db(database, f"SELECT * FROM Collection WHERE collection_name ='{collection}';")
        if query:
            result_list = []
            for i in range(len(query)):
                result_list.append({"uri": "/collections/{}".format(query[i][0]),
                                    "id": int(query[i][0]),
                                    "creation_time": query[i][4],
                                    "indicator": query[i][2]
                                    })
            return result_list, 200
        api.abort(404, "The collection {} not found in data source!".format(collection))

    # question 4, get one specified collection and its data
    elif operation == 'get_1_id':
        col_query = control_db(database,
                                      f"SELECT * "
                                      f"FROM Collection "
                                      f"WHERE collection_name = '{collection}'"
                                      f"AND collection_id = {kwargs['collection_id']};")

        entries_query = control_db(database,
                                   f"SELECT country, date, value "
                                   f"FROM entries "
                                   f"WHERE id = {kwargs['collection_id']};")
        if col_query:
            result = {"id": int(col_query[0][0]),
                      "indicator": col_query[0][2],
                      "indicator_value": col_query[0][3],
                      "creation_time": col_query[0][4],
                      "entries": list()
                      }
            for i in range(len(entries_query)):
                if entries_query[i][2] != "null":
                    result["entries"].append({"country": entries_query[i][0],
                                              "date": int(entries_query[i][1]),
                                              "value": eval(entries_query[i][2])
                                              })
            return result, 200
        return {"message":
                    f"The collection '{collection}' with id {kwargs['collection_id']} not found in data source!"}, 404

    # question 5, get data for year, id and country
    elif operation == 'get_date_country':
        cre_query = control_db(database,
                                  f"SELECT collection_id, indicator, country, date, value "
                                  f"FROM Collection "
                                  f"JOIN entries ON (Collection.collection_id = entries.id) "
                                  f"WHERE collection_id = {kwargs['collection_id']} "
                                  f"AND date = '{kwargs['year']}' "
                                  f"AND country = '{kwargs['country']}';")
        if cre_query:
            return {"id": int(cre_query[0][0]),
                    "indicator": cre_query[0][1],
                    "country": cre_query[0][2],
                    "year": int(cre_query[0][3]),
                    "value": eval(cre_query[0][4])
                    }, 200
        return {"message": f"The given arguments collections = '{collection}', {kwargs} not found in data source!"}, 404

    # question 6, get data for year, id, sort by its value, can be either descent or ascent.
    elif operation == 'get_up_down':
        insert_flag = ''
        if kwargs['flag'] == 'top':  # if get up, it should be reverse sort and limit first values
            insert_flag = 'DESC'

        col_query = control_db(database,
                                      f"SELECT * FROM Collection WHERE collection_name = '{collection}'"
                                      f"AND collection_id = {kwargs['collection_id']};")

        # should use cast otherwise it sorted by string order
        entries_query = control_db(database,
                                   f"SELECT country, date, value "
                                   f"FROM entries "
                                   f"WHERE id = {kwargs['collection_id']} "
                                   f"AND date = '{kwargs['year']}' "
                                   f"AND value != 'None' "
                                   f"GROUP BY country, date, value "
                                   f"ORDER BY CAST(value AS REAL) {insert_flag} "
                                   f"LIMIT {kwargs['value']};")

        if col_query:
            result = retrieve_json1(col_query, entries_query)
            result.pop("id")
            result.pop("creation_time")
            return result, 200
        api.abort(404, "No data matches your specified arguments in the database!")


# dealing with all post requests, for question 1
def handlepost(database, collection, indicator):
    query = control_db(database, f"SELECT * FROM Collection WHERE indicator = '{indicator}';")
    if query:
        return {"uri": "/collections/{}".format(query[0][0]),
                "id": int(query[0][0]),
                "creation_time": query[0][4],
                "indicator_id": query[0][2]
                }, 200
    else:
        data_page_1 = urlrequest(indicator, 1)
        data_page_2 = urlrequest(indicator, 2)
        if not data_page_1 or not data_page_2:
            api.abort(404, "The indicator {} not found in data source!".format(indicator))
        new_id = re.findall('\\d+', str(control_db(database, 'SELECT MAX(collection_id) FROM Collection;')))
        if not new_id:
            new_id = 1
        else:
            new_id = int(new_id[0]) + 1
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        collection_1 = "INSERT INTO Collection VALUES ({}, '{}', '{}', '{}', '{}');" \
            .format(new_id, collection, data_page_1[0]['indicator']['id'], data_page_1[0]['indicator']['value'],
                    cur_time)
        control_db(database, collection_1)
        entries_table_update(database, new_id, data_page_1)
        entries_table_update(database, new_id, data_page_2)
        new_query = control_db(database, f"SELECT * FROM Collection WHERE indicator = '{indicator}';")
        return {"uri": "/collections/{}".format(new_query[0][0]),
                "id": int(new_query[0][0]),
                "creation_time": new_query[0][4],
                "indicator_id": new_query[0][2]
                }, 201


# dealing with all delete requests, for question 2
def handledelete(database, collection, collection_id):
    query = control_db(database,
                       f"SELECT * FROM Collection WHERE collection_name = '{collection}' "
                       f"AND collection_id = {collection_id};")
    if not query:
        api.abort(404, "The collection {} was NOT FOUND in the database!".format(collection_id))

    else:
        control_db(database, f"DELETE FROM entries WHERE id = {collection_id};")
        control_db(database, f"DELETE FROM Collection WHERE collection_name = '{collection}';")
        return {"message": f"The collection {collection_id} was removed from the database!",
                "id": collection_id}, 200


# importing data, store in database for table collection, called by post handle
def collection_table_update(database, given_id, given_collection_name, data):
    collection_table_update(database, new_id, collection, data_page_1)
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    collection_1 = "INSERT INTO Collection VALUES ({}, '{}', '{}', '{}', '{}');" \
        .format(new_id, collection, data_page_1[0]['indicator']['id'], data_page_1[0]['indicator']['value'],
                cur_time)
    control_db(database, collection_1)


# importing data, store in database for table collection, called by post handler
def entries_table_update(database, given_id, datas):
    entries = "INSERT INTO entries VALUES"
    for data in datas:
        data['country']['value'] = data['country']['value'].replace("'", "")
        entries = entries + f"({given_id}, '{data['country']['value']}', '{data['date']}', '{data['value']}'),"
    entries = entries.rstrip(',') + ';'
    control_db(database, entries)


indicator_model = api.model('POST', {
    'indicator_id': fields.String(required=True,
                                  title='An Indicator ',
                                  description='http://api.worldbank.org/v2/indicators',
                                  example='NY.GDP.MKTP.CD')})
parser = api.parser()
parser.add_argument('q', type=str, help='Query param. Expected format: top5 / bottom20', location='args')


# First-path route class, for question 1 and 3
@api.route("/<string:collections>")
class FirstPath(Resource):
    @api.response(200, 'OK')
    @api.response(500, 'Invalid parameter')
    @api.expect(indicator_model)
    def post(self, collections):
        if not api.payload or 'indicator_id' not in api.payload:
            api.abort(404, "Please check if the indicator_id is given!")
        return handlepost('z5244467.db', collections, indicator=api.payload['indicator_id'])

    def get(self, collections):
        return handleget('z5244467.db', collections, 'getALLid')


# Second-paths route class, for question 2 and 4
@api.route("/<string:collections>/<int:id>")
class SecondPath(Resource):
    @api.response(200, 'OK')
    @api.response(201, 'Created')
    @api.response(500, 'Invalid parameter')
    def delete(self, collections, id):
        return handledelete('z5244467.db', collections, collection_id=id)

    def get(self, collections, id):
        return handleget('z5244467.db', collections, 'get_1_id', collection_id=id)


# Third-paths route class, for question 5
@api.route("/<string:collections>/<int:id>/<int:year>/<string:country>")
class ThirdPath(Resource):
    @api.response(200, 'OK')
    @api.response(201, 'Created')
    @api.response(500, 'Invalid parameter')
    def get(self, collections, id, year, country):
        return handleget('z5244467.db', collections, 'get_date_country', collection_id=id,
                         year=year, country=country)


# Third route class, with argument required, for question 6
@api.route("/<string:collections>/<int:id>/<int:year>")
class FourthPath(Resource):
    @api.doc(parser=parser)
    @api.response(200, 'OK')
    @api.response(201, 'Created')
    @api.response(500, 'Invalid parameter')
    def get(self, collections, id, year):
        query = parser.parse_args()['q']
        return handlerequestq6('z5244467.db', collections, collection_id=id,
                               year=year, query=query)

if __name__ == "__main__":
    create_db('z5244467.db')
    app.run(host='127.0.0.1', port=5050, debug=True)

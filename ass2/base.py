from flask import Flask
from flask_restplus import Resource, Api, fields
import sqlite3
import os
import json
import time
import re
import urllib.request as req

app = Flask(__name__)
api = Api(app, title="API for World Bank Economic Indicators.", description=" by Chen Wu z5244467")


# database control, for executing SQL command and fetching results
def control_db(database, command):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    if len(re.findall(';', command)) > 1:
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
                     'CREATE TABLE storage('
                     'id INTEGER NOT NULL,'
                     'country VARCHAR(100),'
                     'date VARCHAR(10),'
                     'value VARCHAR(100),'
                     'CONSTRAINT storage_fkey FOREIGN KEY (id) REFERENCES Collection(collection_id));'
                     )
    return True


# remote API request, fetching data from worldbank API
def urlrequest(indicator, page, start=2012, end=2017, content_format='json'):
    url = f'http://api.worldbank.org/v2/countries/all/indicators/' + \
          f'{indicator}?date={start}:{end}&format={content_format}&page={page}'
    resource = req.Request(url)
    data = req.urlopen(resource).read()
    if re.findall('Invalid value', str(data), flags=re.I):
        return False
    return json.loads(data)[1]

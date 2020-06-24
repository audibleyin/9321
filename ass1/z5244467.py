import ast
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

studentid = os.path.basename(sys.modules[__name__].__file__)


#################################################
# Your personal methods can be here ...
def fun_8(x):
    characters = list()
    dic_list = eval(x)
    for dic in dic_list:
        character = dic['character']
        if len(character) != 0:
            characters.append(character)
    characters = sorted(characters)
    characters_str = ', '.join(characters)
    return characters_str
#################################################
def fun_9(x):
    c = x.count(',')
    return c

def fun_11(x):
    x = x.replace('\'', '\"')
    l = json.loads(x)
    name_type = list()
    for type in l:
        name_type.append(type['name'])
    return name_type
def scatterLegend(data, labels, x, y):

    pass


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))
    if other is not None:
        print(question, other)
    if output_df is not None:
        print(output_df.head(5).to_string())


def question_1(movies, credits):
    """
    :param movies: the path for the movie.csv file
    :param credits: the path for the credits.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    movies = pd.read_csv(movies)
    credits = pd.read_csv(credits)
    df1 = pd.merge(movies, credits, on = 'id')
    #################################################
    df1.to_csv("df111.csv")

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df2 = df1[['id', 'title', 'popularity', 'cast', 'crew', 'budget', 'genres', 'original_language', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'vote_average', 'vote_count']]

    #################################################

    log("QUESTION 2", output_df=df2, other=(len(df2.columns), sorted(df2.columns)))
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################
    df3 = df2.set_index(['id'])

    log("QUESTION 3", output_df=df3, other=df3.index.name)
    return df3


def question_4(df3):
    """
    :param df3: the dataframe created in question 3
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df3.drop(df3[df3.budget == 0].index, inplace=True)
    df4 = df3
    #################################################
    log("QUESTION 4", output_df=df4, other=(df4['budget'].min(), df4['budget'].max(), df4['budget'].mean()))
    return df4


def question_5(df4):
    """
    :param df4: the dataframe created in question 4
    :return: df5
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df5 = df4.copy()
    df5['success_impact'] = df4[["revenue", "budget"]].apply(lambda x: (x.revenue - x.budget)/x.budget,
                                                                          axis=1)
   #################################################

    log("QUESTION 5", output_df=df5,
        other=(df5['success_impact'].min(), df5['success_impact'].max(), df5['success_impact'].mean()))
    return df5


def question_6(df5):
    """
    :param df5: the dataframe created in question 5
    :return: df6
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df6 = df5.copy()
    df6.popularity = 100 * (df5.popularity - df5.popularity.min()) / (df5.popularity.max() - df5.popularity.min())
    #################################################

    log("QUESTION 6", output_df=df6, other=(df6['popularity'].min(), df6['popularity'].max(), df6['popularity'].mean()))
    return df6


def question_7(df6):
    """
    :param df6: the dataframe created in question 6
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df7 = df6.copy()
    df7['popularity'] = df6['popularity'].astype('int16')
    #################################################

    log("QUESTION 7", output_df=df7, other=df7['popularity'].dtype)
    return df7


def question_8(df7):
    """
    :param df7: the dataframe created in question 7
    :return: df8
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df8 = df7.copy()
    df8['cast'] = df7['cast'].apply(lambda x: fun_8(x))
    #################################################
    log("QUESTION 8", output_df=df8, other=df8["cast"].head(10).values)
    return df8


def question_9(df8):
    """
    :param df9: the dataframe created in question 8
    :return: movies
            Data Type: List of strings (movie titles)
            Please read the assignment specs to know how to create the output
    """
    #################################################
    # Your code goes here ...
    movies = list()
    df9 = df8.copy()
    df9['count'] = df8['cast'].apply(lambda x: fun_9(x))
    df9 = df9.sort_values('count', ascending=False)
    df9.to_csv('df9.csv')
    for movie in df9['title']:
        movies.append(movie)
        if len(movies) > 9:
            break
    #################################################

    log("QUESTION 9", output_df=None, other=movies)
    return movies


def question_10(df8):
    """
    :param df8: the dataframe created in question 8
    :return: df10
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df10 = df8.copy()
    df10['date'] = pd.to_datetime(df8['release_date'])
    df10 = df10.set_index('date')
    df10 = df10.sort_index(ascending=False)
    #################################################
    log("QUESTION 10", output_df=df10, other=df10["release_date"].head(5).to_string().replace("\n", " "))
    return df10


def question_11(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    name = list()
    tmp = df10['genres'].apply(lambda x: fun_11(x))
    for l in tmp:
        for i in l:
            name.append(i)
    name_dic = dict.fromkeys(list(set(name)))
    for i in list(set(name)):
        name_dic[i] = name.count(i)
    value = list(name_dic.values())
    plt.figure(figsize=(16, 9), dpi=100)
    plt.pie(x=value, labels=list(set(name)), autopct='%.1f%%', pctdistance=1.1, labeldistance=1.2)

    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_12(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    name_list = []
    for l in df10['production_countries'].apply(lambda x: fun_11(x)):
        for i in l:
            name_list.append(i)
    labels = list(set(name_list))
    labels = sorted(labels)
    dic = dict.fromkeys(labels)
    for i in labels:
        dic[i] = name_list.count(i)
    value = list(dic.values())
    plt.figure(figsize=(16,9), dpi=100)
    plt.xticks(rotation=-60)
    plt.title('Production Countries')
    plt.bar(labels, value, color='steelblue')
    #################################################

    plt.savefig("{}-Q12.png".format(studentid))


def question_13(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    language = sorted(list(set(list(df10['original_language']))))


    color = dict.fromkeys(language)
    colors ={
        'Crimson':              '#DC143C',
        'LavenderBlush':        '#FFF0F5',
        'Orchid':               '#DA70D6',
        'Purple':               '#800080',
        'Indigo':               '#4B0082',
        'MediumBlue':           '#0000CD',
        'LightSlateGray':       '#778899',
        'DoderBlue':            '#1E90FF',
        'MediumAquamarine':     '#00FA9A',
        'SpringGreen':          '#3CB371',
        'SeaGreen':             '#2E8B57',
        'DarkSeaGreen':         '#8FBC8F',
        'forestgreen':          '#228B22',
        'Black':                '#000000',
        'NavajoWhite':          '#FFDEAD',
    }
    cols = list()
    for c in colors.values():
        cols.append(c)
    n = 0
    for i in color.keys():
        color[i] = cols[n]
        n += 1
    plt.figure(figsize=(20, 20), dpi=250)

    plt.title('vote_average vs.success_impact')
    plt.xlabel("vote_average")
    plt.ylabel("success_impact")
    plt.grid(True)

    t1 = plt.scatter(df10['vote_average'],df10['success_impact'], c= '#800080')
    t2 = plt.scatter(df10['vote_average'],df10['success_impact'], c= '#FFDEAD')
    t3 = plt.scatter(df10['vote_average'],df10['success_impact'], c= '#DA70D6')
    t4 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#4B0082')
    t5 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#0000CD')
    t6 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#8FBC8F')
    t7 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#DC143C')
    t8 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#FFF0F5')
    t9 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#3CB371')
    t10 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#000000')
    t11 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#778899')
    t12 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#228B22')
    t13 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#00FA9A')
    t14 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#1E90FF')
    t15 = plt.scatter(df10['vote_average'], df10['success_impact'], c='#2E8B57')

    plt.legend(handles=[t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15],\
               labels= ['en', 'zh', 'de', 'es', 'fi', 'no', 'af', 'da', 'ko', 'sv', 'fr', 'pt', 'ja', 'it', 'nl'], loc = 'best')
    plt.scatter(df10['vote_average'], df10['success_impact'], c=df10['original_language'].map(color))


    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("movies.csv", "credits.csv")
    df2 = question_2(df1)
    df3 = question_3(df2)
    df4 = question_4(df3)
    df5 = question_5(df4)
    df6 = question_6(df5)
    df7 = question_7(df6)
    df8 = question_8(df7)
    movies = question_9(df8)
    df10 = question_10(df8)
    question_11(df10)
    question_12(df10)
    question_13(df10)

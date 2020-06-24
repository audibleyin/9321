import pandas as pd
import sys
import ast
import json
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import *
from scipy.stats import pearsonr
from sklearn.ensemble import RandomForestRegressor
if not len(sys.argv) == 3:
    print("need path1 and path2")
    sys.exit()

df = pd.read_csv(sys.argv[1])  # sys.argv[1]
test = pd.read_csv(sys.argv[2])  # sys.argv[2]
df2 = df[['cast', 'crew', 'budget', 'runtime','genres','keywords','release_date','original_title']]
df_test = test[['cast', 'crew', 'budget', 'runtime','genres','keywords','release_date','original_title']]

# clean data in df
month = df2['release_date']
mon_list = []
for m in range(len(month)):
    year,mon,date = month[m].split('-')
    mon_list.append(mon)
for i in range(len(df2['release_date'])):
    df2['release_date'][i] = mon_list[i]
Key_result = df2['keywords']
Key_list = []
for i in range(len(Key_result)):
    t = len(Key_result[i])
    Key_list.append(t)

for i in range(len(df2['keywords'])):
    df2['keywords'][i] = Key_list[i]
for i in range(len(df2['cast'])):
    target_cast = ast.literal_eval(df2['cast'][i])
    df2['cast'][i] = target_cast[0]['name']
for i in range(len(df2['crew'])):
    target_cast = ast.literal_eval(df2['crew'][i]) 
    for j in target_cast:
        if j['job'] == 'Director':
            df2['crew'][i] = j['name']
for i in range(len(df2['genres'])):
    target_cast = ast.literal_eval(df2['genres'][i])
    df2['genres'][i] = target_cast[0]['name']
# g_res1 = df2['genres']
# g_l1 = []
# for i in range(len(g_res1)):
#     t = len(g_res1[i])
#     g_l1.append(t)
# for i in range(len(df2['genres'])):
#     df2['genres'][i] = g_l1[i]     
print(df2.head(10))
# clean data in df_test
for i in range(len(df_test['cast'])):
    target_cast = ast.literal_eval(df_test['cast'][i])
    df_test['cast'][i] = target_cast[0]['name']
for i in range(len(df_test['genres'])):
    target_cast = ast.literal_eval(df_test['genres'][i])
    df_test['genres'][i] = target_cast[0]['name']
for i in range(len(df_test['crew'])):
    target_cast = ast.literal_eval(df_test['crew'][i]) 
    for j in target_cast:
        if j['job'] == 'Director':
            df_test['crew'][i] = j['name']
k_res = df_test['keywords']
k_list = []
for i in range(len(k_res)):
    t = len(k_res[i])
    k_list.append(t)            
for i in range(len(df_test['keywords'])):
    df_test['keywords'][i] = k_list[i]
# g_res = df_test['genres']
# g_l = []
# for i in range(len(g_res)):
#     t = len(g_res[i])
#     g_l.append(t)
# for i in range(len(df_test['genres'])):
#     df_test['genres'][i] = g_l[i]
month = df_test['release_date']
mon_list = []
for m in range(len(month)):
    year,mon,date = month[m].split('-')
    mon_list.append(mon)
for i in range(len(df_test['release_date'])):
    df_test['release_date'][i] = mon_list[i]
# print(df2.head(10))
# print(df2['crew'])
# use labelencoder to encode
df2[['cast','crew','genres','original_title']]=df2[['cast','crew','genres','original_title']].apply(LabelEncoder().fit_transform)
part1_result = df2.copy()
print(part1_result)
df_test[['cast','crew','genres','original_title']]=df2[['cast','crew','genres','original_title']].apply(LabelEncoder().fit_transform)
df_test_x = df_test.copy()
print(df_test_x)
part1_test = df[['revenue']]
df3 = df2[['cast','crew', 'budget', 'runtime','genres','keywords','release_date','original_title']] 
# print(df3.head(10)) 
part1 = LogisticRegression().fit(df3,part1_test)
part1_result = part1.predict(df_test_x)

movie_id = test['movie_id']

df5 = pd.DataFrame()
df5['movie_id'] = test['movie_id']
df5['predicted_revenue'] = part1_result 
df5.to_csv("z5244467.PART1.output.csv",index=False)

# print(result)
# print(test.revenue)

# print(type(test.revenue))
# ser = test.revenue.to_numpy('float64')
# print(ser)
# print(type(ser))
# ser = ser.tolist()
# print(ser)
# part1_result_list= part1_result.tolist()
# print(part1_result_list)
# result_list = list()
# result_list.extend([x[0] for x in part1_result_list])
# print(result_list)
# part1_result_1 = np.array(result_list)

MSR = mean_squared_error(test.revenue,part1_result)
print(MSR)
pccs = pearsonr(test.revenue,part1_result)
print(pccs)
zid = list()
zid.append('z5244467')
MSR_list = list()
MSR_list.append(round(MSR,2))
pccs_list = list(pccs)
df7 = pd.DataFrame()
df7['zid'] = zid
df7['MSR'] = MSR_list
df7['correlation'] =round(pccs_list[0], 2)  
df7.to_csv("z5244467.PART1.summary.csv",index=False)

part2_test = df['rating']
part2 = KNeighborsClassifier(n_neighbors=7)
part2.fit(df3,part2_test)
knn_result = part2.predict(df_test_x)
df8 = pd.DataFrame()
df8['movie_id'] = test['movie_id']
df8['predicted_rating'] = knn_result
df8.to_csv("z5244467.PART2.output.csv",index=False)

# print(test.rating)
# ser = ser.tolist()
# print(ser)
# print('knn:',knn_result)
# print(type(knn_result))
# part2_result = knn_result.tolist()
# print(part2_result)
# kresult_list = list()
# kresult_list.extend([x[0] for x in part2_result])
# print(kresult_list)
# part2_result_1 = np.array(kresult_list)

precision = precision_score(test.rating,knn_result, average=None)
print('Average precision-recall score: {0:0.2f}'.format(precision[0]))
recall = recall_score(test.rating,knn_result, average=None)
accuracy = accuracy_score(test.rating,knn_result)
print('accuracy score: {0:0.2f}'.format(accuracy))
pre = list()
pre.append(round(precision[0],2))
re = list()
re.append(round(recall[1],2))
acc = list()
acc.append(round(accuracy,2))
df9 = pd.DataFrame()
df9['zid'] = zid
df9['average_precision'] = pre
df9['average_recall'] = re
df9['accuracy'] = acc
df9.to_csv("z5244467.PART2.summary.csv",index=False)
import pandas as pd

df1 = pd.read_csv('dataset1.csv')
df2 = pd.read_csv('dataset2.csv')
df3 = pd.merge(df1, df2, on = 'Device ID')
df3.to_csv("df3.csv")
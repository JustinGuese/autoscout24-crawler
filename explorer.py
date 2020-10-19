import pandas as pd

data = pd.read_csv("/home/justin/Documents/python/autoscoutcrawler/data/autos/2020-10-19_18_01_52_502709.csv",delimiter=";")

print(data.describe())
print(data.head())
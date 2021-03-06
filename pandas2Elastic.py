import elasticsearch 
from tqdm import tqdm
import pandas as pd

# df is a dataframe or dataframe chunk coming from your reading logic

df = pd.read_csv("data/autos/largeDF.csv.gz",compression="gzip")
df = df[["Modell","Marke","Garantie","country","Zustand", "Zylinder","Kraftstoff","Erstzulassung", "Außenfarbe","Innenausstattung","Karosserieform","Anzahl Türen","Sitzplätze","Getriebeart","Gänge",'Hubraum', 'Kraftstoff', 'Schadstoffklasse', 'haendler', 'privat',"price"]]
# store df again cleaned
df.to_csv("data/autos/largeDF.csv.gz",compression="gzip",index=False)


es = elasticsearch.Elasticsearch()


dindawork = []
for i,entry in tqdm(df.iterrows(),total=len(df)):
    try:
        entry = entry.to_dict()
        es.index(index="autoscout-singlecar", body=entry)
    except elasticsearch.exceptions.RequestError as e:
        dindawork.append([i,entry])

print("DINDT WORK: ",dindawork)
print(len(dindawork)," of ",len(df)," items failed.")
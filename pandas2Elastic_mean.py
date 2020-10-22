import elasticsearch 
from tqdm import tqdm
import pandas as pd

# df is a dataframe or dataframe chunk coming from your reading logic

df = pd.read_csv("MostCommonEntrieswZScore.csv")
df = df[["Modell","Marke","Garantie","country","Zustand", "Zylinder","Kraftstoff","Erstzulassung", "Außenfarbe","Innenausstattung","Karosserieform","Anzahl Türen","Sitzplätze","Getriebeart","Gänge",'Hubraum', 'Kraftstoff', 'Schadstoffklasse', 'haendler', 'privat',"price","predicted_price","zscore"]]
# store df again cleaned
df.to_csv("MostCommonEntrieswZScore.csv",index=False)


es = elasticsearch.Elasticsearch()


dindawork = []
for i,entry in tqdm(df.iterrows(),total=len(df)):
    try:
        entry = entry.to_dict()
        es.index(index="autoscout-average", body=entry)
    except elasticsearch.exceptions.RequestError as e:
        dindawork.append([i,entry])

print("DINDT WORK: ",dindawork)
print(len(dindawork)," of ",len(df)," items failed.")
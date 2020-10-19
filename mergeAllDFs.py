import pandas as pd
import os
import numpy as np

folder=r'./data/autos/'
dfs = []

defcolumns = []
removed = ['Scheckheftgepflegt', 'Antriebsart', 'Länderversion', 'Feinstaubplakette']
selection = ["url","country","date","Zustand","Garantie","Marke","Modell","Angebotsnummer","Außenfarbe","Lackierung","Farbe laut Hersteller","Innenausstattung","Karosserieform","Anzahl Türen","Sitzplätze","Schlüsselnummer","Getriebeart","Gänge","Hubraum","Kraftstoff","Schadstoffklasse","haendler","privat","ort","price","ausstattung_liste","Erstzulassung","Zylinder","Leergewicht"]

for filename in os.listdir(folder):

    print(filename)
    df = pd.read_csv(folder+filename, delimiter=";")
    for col in selection:
        if col not in df.columns:
            df[col] = 0
    df = df[selection]
    
    dfs.append(df)

result = pd.concat(dfs)
print("size before cleanup: ",result.shape)
result = result.drop_duplicates()
result = result.dropna(thresh=20)
print("size after cleanup: ",result.shape)
result.to_csv(folder+"largeDF.csv")
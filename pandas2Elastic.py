import pandas as pd
from espandas import Espandas

data = pd.read_csv("data/autos/largeDF.csv.gz",compression="gzip")
data = data[["Modell","Marke","Garantie","country","Zustand", "Zylinder","Kraftstoff","Erstzulassung", "Außenfarbe","Innenausstattung","Karosserieform","Anzahl Türen","Sitzplätze","Getriebeart","Gänge",'Hubraum', 'Kraftstoff', 'Schadstoffklasse', 'haendler', 'privat',"price"]]

INDEX = 'autoscout'
TYPE = 'car'
esp = Espandas()
esp.es_write(data, INDEX, TYPE)
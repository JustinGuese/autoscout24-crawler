import joblib 
import pandas
import json
import pandas as pd

model_name = "randomforest_fullytrained.sav"
scaler_name = "scaler_fullytrained.sav"


def lambda_handler(event, context):
    # Parse input
    #body = event['body']
    #input = json.loads(body)['data']
    df = pd.read_json(event,orient="records")
    #print(df.head())
    print(df.info())
    # Download pickled model from S3 and unpickle
    #s3.download_file(s3_bucket, model_name, temp_file_path)
    with open(model_name, 'rb') as f:
        model = joblib.load(f)
    with open(scaler_name, 'rb') as f:
        scaler = joblib.load(f)

    df["price"] = 0 # needed as scaler likes price
    def preprocess(data,scaler):
        # have to be really restrictive with data columns
        obj_df = data[['Modell', 'Marke', 'Garantie', 'country', 'Zustand', 'Kraftstoff',
       'Außenfarbe', 'Innenausstattung', 'Karosserieform', 'Getriebeart',
       'Hubraum', 'Schadstoffklasse', 'haendler', 'privat']]
        num_df = data[['Zylinder', 'Erstzulassung', 'Anzahl Türen', 'Sitzplätze', 'Gänge',
       'price']]
        num_df = num_df.astype(float)
        print(num_df.shape,num_df.columns)
        obj_df = pd.get_dummies(obj_df)
        cols = num_df.columns
        num_df = scaler.transform([num_df.values])
        num_df = pd.DataFrame(num_df,columns=cols)
        print(np.shape(num_df),np.shape(obj_df))
        data = pd.concat([obj_df,num_df])
        return data
    data,preprocess(df,scaler)
    print(data.head())
    pred = model.predict([data])[0]


cols = ['Modell', 'Marke', 'Garantie', 'country', 'Zustand', 'Zylinder',
       'Kraftstoff', 'Erstzulassung', 'Außenfarbe', 'Innenausstattung',
       'Karosserieform', 'Anzahl Türen', 'Sitzplätze', 'Getriebeart', 'Gänge',
       'Hubraum', 'Schadstoffklasse', 'haendler', 'privat']
values = ['500', 'Abarth', '0', 'Deutschland',
       'Tipp:Prüfe das Fahrzeug bei der Besichtigung auf Mängel. Generell gehen wir bei allen Angeboten von einem guten Fahrzeug-Zustand aus.',
       4.0, 'Benzin', 2010.0, 'Grau', 'Vollleder, Sonstige', 'Kleinwagen',
       2.0, 4.0, 'Schaltgetriebe', 5.0, '1.368 cm³', 'Euro 5',
       '1', '0']

#7990.0, 8022.24800000005, 0.30827273340836886]
data =  pd.DataFrame([values],columns=cols)
js = data.to_json(orient="records")


lambda_handler(js,None)

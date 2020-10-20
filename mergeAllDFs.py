import pandas as pd
import os
import numpy as np
import glob

S3UPLOAD = True

if S3UPLOAD:
    import boto3
    from botocore.exceptions import NoCredentialsError
    s3 = boto3.client('s3')
    s3.download_file('datafortress-frankfurt', 'largeDF.csv.gz', folder+'largeDF.csv.gz')
    # load largeDF



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

# load old
old = pd.read_csv(folder+"largeDF.csv.gz",compression="gzip" )
new = pd.concat([result,old])
new = new.drop_duplicates()
new = new.dropna(thresh=20)


new.to_csv(folder+"largeDF.csv.gz",compression="gzip")
print("New size: ",new.shape)
# remove old
fileList = glob.glob(folder+'*.csv')
for filePath in fileList:
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file : ", filePath)

if S3UPLOAD:
    def upload_to_aws(local_file, bucket, s3_file):

        try:
            s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False


    uploaded = upload_to_aws(folder+'largeDF.csv.gz', 'datafortress-frankfurt', 'largeDF.csv.gz')

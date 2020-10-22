import json
import sklearn
import boto3
import os
import json
import joblib
import pandas as pd
s3 = boto3.client('s3')
s3_bucket = os.environ['s3_bucket']
model_name = os.environ['model_name']
scaler_name = os.environ['scaler_name']
temp_file_path = '/tmp/' + model_name
from sklearn.ensemble import RandomForestRegressor

def lambda_handler(event, context):
    # Parse input
    body = event['body']
    input = json.loads(body)['data']
    df = pd.json_normalize(input)
    print(df.head())

    # Download pickled model from S3 and unpickle
    s3.download_file(s3_bucket, model_name, temp_file_path)
    with open('/tmp/' + model_name, 'rb') as f:
        model = joblib.load(f)
    with open('/tmp/' + scaler_name, 'rb') as f:
        scaler = joblib.load(f)

    def preprocess(data,scaler):
        obj_df = data.select_dtypes(include=['object']).copy()
        num_df = data.select_dtypes(include=['float64']).copy()
        obj_df = pd.get_dummies(obj_df)
        cols = num_df.columns
        num_df = scaler.transform(num_df)
        num_df = pd.DataFrame(num_df,columns=cols)
        data = pd.concat([obj_df,num_df],axis=1)
        return data
    data,preprocess(df,scaler)
    pred = model.predict([data])[0]
    

    # Predict class

    prediction = model.predict([[input]])[0]
    return {
        "statusCode": 200,
        "body": json.dumps({
            "prediction": str(prediction),
        }),
    }
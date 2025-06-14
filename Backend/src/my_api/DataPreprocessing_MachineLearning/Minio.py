from minio import Minio
from os import getenv
from minio.error import S3Error
import joblib, io
import json
from dotenv import load_dotenv
import pandas as pd
import os


def minio_client():
    load_dotenv()
    endpoint = "minio:9000"
    return Minio(
        endpoint,
        access_key=getenv("MINIO_ACCESS_KEY"),
        secret_key=getenv("MINIO_SECRET_KEY"),
        secure=False
    )

def get_csv_minio(client):
    bucket_name = "model-bucket2"
    object_name = "data/animalsLabeled.csv"
    
    found = client.bucket_exists(bucket_name)
    if not found:
        raise ValueError(f"Bucket '{bucket_name}' does not exist.")
    
    response = client.get_object(bucket_name, object_name)
    csv_data = response.read().decode('utf-8')
    response.close()
    response.release_conn()
    
    csv_df = pd.read_csv(io.StringIO(csv_data))
    return csv_df

def upload_model_minio(client):
    
    base_dir = os.path.dirname(__file__)  # ruta correcta
    source_file = os.path.join(base_dir, "models", "decision_tree_model.pkl")
    
    bucket_name = "model-bucket2"
    destination_file = "decision_tree_model.pkl"

    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print(f"Created bucket {bucket_name}")
    


    client.fput_object(bucket_name, destination_file, source_file)
    print(f" 2º Model updaded as '{destination_file}'to bucket '{bucket_name}'.")


def get_model_minio(client):
    bucket_name = "model-bucket2"
    object_name = "decision_tree_model.pkl"
    
    found = client.bucket_exists(bucket_name)
    if not found:
        raise ValueError(f"Bucket '{bucket_name}' no existe.")
    
    response = client.get_object(bucket_name, object_name)
    model = joblib.load(io.BytesIO(response.read()))
    response.close()
    response.release_conn()
    return model

def upload_paramModel_minio(client):
    bucket_name = "model-bucket2"
    destination_file = "data/decision_tree_model_params.json"
    model = get_model_minio(client)

     # Extract parameters as a dict
    params = model.get_params()

    
    #Create a BytesIO object after converting the dict to JSON
    json_bytes = json.dumps(params, indent=4).encode('utf-8')
    bytes_io = io.BytesIO(json_bytes)

   # Upload to MinIO using put_object
    client.put_object(
        bucket_name,
        destination_file,
        bytes_io,
        length=len(json_bytes),
        content_type='application/json'
    )
    print(f" 4º Model parameters uploaded as '{destination_file}' to bucket '{bucket_name}'.")

def upload_csv_minio(client):
    base_dir = os.path.dirname(__file__)
    source_file = os.path.join(base_dir, "data", "animalsLabeled.csv")

    bucket_name = "model-bucket2"
    destination_file = "data/animalsLabeled.csv"

    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print(f"Created bucket {bucket_name}")

    client.fput_object(bucket_name, destination_file, source_file)
    print(f" 3º CSV uploaded as '{destination_file}' to bucket '{bucket_name}'.")
    
def main():
    try:
        client = minio_client()
        print(" 1º MinIO client initialized successfully.")
        upload_model_minio(client)
        upload_csv_minio(client)
        upload_paramModel_minio(client)

        print(" All tasks completed successfully.")

    except S3Error as exc:
        print(" MinIO error:", exc)

if __name__ == "__main__":
    main()

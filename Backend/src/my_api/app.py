from fastapi import FastAPI, HTTPException
import pandas as pd
from typing import List
from my_api.models import new_animal, animal_prediction
from my_api.DataPreprocessing_MachineLearning import get_model_minio ,get_csv_minio,train_model,save_model_local,upload_model_minio,upload_csv_minio,predict_train
from dotenv import load_dotenv
from minio import Minio
from os import getenv

app= FastAPI()

def minio_client():
    load_dotenv()
    return Minio(
        "minio:9000",
        access_key=getenv("MINIO_ACCESS_KEY"),
        secret_key=getenv("MINIO_SECRET_KEY"),
        secure=False
    )
    
client = minio_client()
    
@app.get("/api/v1/get/model",summary="Get the lastest model", description="This endpoint returns the latest trained model from MinIO.", response_model= object)
def get():
    try:
        model = get_model_minio(client)

        model_info = {
            "modelo": type(model).__name__,
            "parametros": model.get_params()
        }

        return model_info

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el modelo: {str(e)}")

@app.post("/api/v1/post/train",summary="Train a new model", description="This endpoint trains a new model with the provided data and saves it to MinIO.", response_model=object)
def post(data: List[new_animal]):
    try:
        csv_old= get_csv_minio(client)
        csv_newAnimal= [item.model_dump() for item in data]
        # Convert the input data to a DataFrame
        
        new_data_df = pd.concat([csv_old, pd.DataFrame(csv_newAnimal)], ignore_index=True) 
        new_data_df.to_csv("my_api/DataPreprocessing_MachineLearning/data/animalsLabeled.csv", index=False)
        upload_csv_minio(client)
        
        #Create a new model with the new and old data
        model_new= train_model(new_data_df)
        #Save the new model locally
        save_model_local(model_new,"my_api/DataPreprocessing_MachineLearning/models/decision_tree_model.pkl")
        #Upload the new model to MinIO from local storage(before step)
        upload_model_minio(client)
        
        return {"status": 200, "message": "New animal added, model retrained and uploaded successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")
 
@app.post("/api/v1/predict", summary="Predict animal type", description="This endpoint predicts the type of animal based on the provided features.", response_model=List[str])
def predict(data: List[animal_prediction]):
    try:   
        model = get_model_minio(client)
        
        
        data_dicts =  [item.model_dump() for item in data]
        data_predict = pd.DataFrame(data_dicts)
        
        predictions = predict_train(model,  data_predict)
        
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
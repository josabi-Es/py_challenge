import requests
from pydantic import BaseModel
from models import animal_prediction , new_animal
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

url_data= os.getenv("URL_DATA_SERVICE")

BASE_URL = os.getenv("BASE_URL")
url_train = f"{BASE_URL}/api/v1/post/train"
url_predict = f"{BASE_URL}/api/v1/predict"
url_get_info = f"{BASE_URL}/api/v1/get/model"


def retrieve_challenge_data(n: int, seed: int) -> list[animal_prediction]:
    """Retrieve a batch of challenge data from the data service

    :param n: The number of data points to retrieve
    :param seed: The seed to use for the random number generator

    :return: A list of AnimalCharacteristics instances"""
    response = requests.post(url_data, json={"number_of_datapoints": n, "seed": seed} )
    response.raise_for_status()
    if response.ok:
        return [animal_prediction(**data) for data in response.json()]
    
    
def train_model(animal: new_animal):
    data_dict = [animal.model_dump()]  
    response = requests.post(url_train, json=data_dict)  
    response.raise_for_status()
    if response.ok:
        return response.json() 
    else:
        raise Exception("Failed to train model")

def predict(animal: animal_prediction):
    
    data_dicts = [animal.model_dump()]

    response = requests.post(url_predict, json=data_dicts)
    response.raise_for_status()
    if response.ok:
        return response.json()
    else:
        raise Exception("Failed to get prediction")

def get_info_model():
    response = requests.get(url_get_info)
    response.raise_for_status()
    if response.ok:
        return response.json()
    else:
        raise Exception("Failed to get model information") 

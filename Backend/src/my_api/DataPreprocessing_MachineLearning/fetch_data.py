import requests
import pandas as pd

def main():
    url = "http://data-service:8777/api/v1/animals/data"
    payload = {"seed": 42, "number_of_datapoints": 1000}
    response = requests.post(url, json=payload)
    df = pd.DataFrame(response.json())
    df.to_csv("my_api/DataPreprocessing_MachineLearning/data/animals.csv", index=False)
    print("Data fetched and saved to data/animals.csv")

if __name__ == "__main__":
    main()
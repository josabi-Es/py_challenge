import numpy as np
import pandas as pd


def main():
    data = pd.read_csv("my_api/DataPreprocessing_MachineLearning/data/animalsClean.csv")

    conditions = [
        # Kangaroo
        (data["walks_on_n_legs"] == 2) & 
        (data["has_wings"] == False) & 
        (data["has_tail"] == True) & 
        (data["weight"] < 150),

        # Elephant
        (data["walks_on_n_legs"] == 4) & 
        (data["has_wings"] == False) & 
        (data["has_tail"] == True) & 
        (data["weight"] > 900),

        # Dogs
        (data["walks_on_n_legs"] == 4) & 
        (data["has_wings"] == False) & 
        (data["has_tail"] == True) & 
        (data["weight"] < 100),

        # Chicken
        (data["walks_on_n_legs"] == 2) & 
        (data["has_wings"] == True) & 
        (data["has_tail"] == True) &
        (data["weight"] < 10)
    ]

    values = [1, 2, 3, 4]
    data["label"] = np.select(conditions, values, default=0)


    dataLabel = data.drop(data[data["label"] == 0].index)
    dataLabel.to_csv("my_api/DataPreprocessing_MachineLearning/data/animalsLabeled.csv", index=False)

    print("Data labeled and saved to data/animalsLbaeled.csv")
      
if __name__ == "__main__":
    main()
import pandas as pd

def main():
    data = pd.read_csv("my_api/DataPreprocessing_MachineLearning/data/animals.csv", header=0)

    # Eliminate duplicates
    data = data.drop_duplicates()

    # Eliminate missing values
    data.dropna(inplace=True)

    # Convert height and weight to numeric
    data["height"] = pd.to_numeric(data["height"], errors="coerce")
    data["weight"] = pd.to_numeric(data["weight"], errors="coerce")

    # Confirm that height and weight are numeric values
    data["height"] = data["height"].astype(float)
    data["weight"] = data["weight"].astype(float)

    # Check for NaN values
    print(f"NaNs in height: {data['height'].isna().sum()}")
    print(f"NaNs in weight: {data['weight'].isna().sum()}")

    # Eliminate values with 1, 3 or 5 legs
    data = data.drop(data[data["walks_on_n_legs"].isin([1, 3, 5])].index)

    # Eliminate values without wings and tails
    data = data.drop(data[(data["has_wings"] == 0) & (data["has_tail"] == 0)].index)

    # Eliminate values with wings but without tails
    data = data.drop(data[(data["has_wings"] == 1) & (data["has_tail"] == 0)].index)

    # Eliminate animals with height more than 4.5 m
    data = data.drop(data[data["height"] > 4.5].index)

    data.to_csv("my_api/DataPreprocessing_MachineLearning/data/animalsClean.csv", index=False)

    print("Data clean and saved to data/animalsClean.csv")

if __name__ == "__main__":
    main()

#my_api/DataPreprocessing_MachineLearning/
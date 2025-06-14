import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib
import os

def train_model(data: pd.DataFrame)-> object:
    '''
    Train a Decision Tree model using the provided dataset.
    '''
    # Split features and target
    X = data.drop("label", axis=1)
    y = data["label"]

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define hyperparameter grid
    param_grid = {
        'criterion': ['gini', 'entropy', 'log_loss'],
        'max_depth': [3, 5, 7, 10, 15],
        'min_samples_leaf': [1, 5, 10],
        'max_leaf_nodes': [10, 20, 30]
    }

    # Grid search with cross-validation
    grid_search = GridSearchCV(DecisionTreeClassifier(),param_grid,scoring='accuracy',cv=5,n_jobs=-1,verbose=1)

    # Fit model
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_

    print(f"Best Params: {best_params}")

    # Train the model with best parameters
    model = DecisionTreeClassifier(
        criterion=best_params['criterion'],
        max_depth=best_params['max_depth'],
        min_samples_leaf=best_params['min_samples_leaf'],
        max_leaf_nodes=best_params['max_leaf_nodes'],
        random_state=5445
    )
    model.fit(X_train, y_train)

    # Evaluate model performance
    print(f"Train accuracy: {model.score(X_train, y_train):.4f}")
    print(f"Test accuracy: {model.score(X_test, y_test):.4f}")

    return model

def save_model_local(model, path: str)-> None:
    """
    Save the trained model to disk using joblib.

    Parameters:
        model: Trained scikit-learn model.
        path (str): File path where the model should be saved.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"Model saved to {path}")

def predict_train (model, data: pd.DataFrame)-> list:
    
    """
    Predict using the trained model.

    Parameters:
        model: Trained scikit-learn model.
        data (pd.DataFrame): DataFrame containing features for prediction.

    Returns:
        np.ndarray: Predictions made by the model.
    """
    
    label_map = {
    1: "Kangaroo",
    2: "Elephant",
    3: "Dog",
    4: "Chicken"
    }
    
    #Predict using the model, returning the predicted numeric labels
    pred_list= model.predict(data)
    # Map numeric predictions to string labels  
    pred_labels = [label_map.get(pred, "Unknown") for pred in pred_list]
    
    return pred_labels

def load_model(path: str)-> object:
        model = joblib.load(path)
        return model
    
def model_params(model):
    """
    Print the parameters of a trained scikit-learn model.
    """
    params = model.get_params()
    return params 

def main():
    # todo el código dentro del if __name__ == "__main__":
    data = pd.read_csv("my_api/DataPreprocessing_MachineLearning/data/animalsLabeled.csv")
    print("Csv file loaded")
    model = train_model(data)
    print("model trained")
    save_model_local(model,"my_api/DataPreprocessing_MachineLearning/models/decision_tree_model.pkl")
    print("model saved in models/decision_tree_model.pkl")
    example= pd.DataFrame([
        {"walks_on_n_legs": 2, "height": 1.8966, "weight": 52.24, "has_wings": False, "has_tail": True},
        {"walks_on_n_legs": 4, "height": 2.8966, "weight": 900, "has_wings": False, "has_tail": True}
    ])
    predictions = predict_train(model, example)
    print("Predictions for example data:", predictions)

if __name__ == "__main__":
    main()
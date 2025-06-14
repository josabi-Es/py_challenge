from my_api.DataPreprocessing_MachineLearning import fetch_data, clean_data, clustering_labeling, Train_Predict_model, Minio

def run_pipeline():
    print("🔹 Step 1: Fetching data...")
    fetch_data.main()
    
    print("🔹 Step 2: Cleaning data...")
    clean_data.main()
    
    print("🔹 Step 3: Clustering & labeling...")
    clustering_labeling.main()
    
    print("🔹 Step 4: Training and predicting...")
    Train_Predict_model.main()
    
    print("🔹 Step 5: Uploading to MinIO...")
    Minio.main()

    print("Pipeline finished successfully.")

if __name__ == "__main__":
    run_pipeline()

# 🐾 Animal Classifier - End-to-End ML Application 🦘🐘🐔🐶
This project is a fully containerized **end-to-end machine learning application** built with Python. It classifies animals into four categories: **Elephant, Kangaroo, Dog, and Chicken** based on a set of numeric features.

It covers the entire ML lifecycle: data generation, preprocessing, model training, API deployment with FastAPI, and a user-friendly dashboard with Streamlit.

## 🚀 Project Components

- **Data Service**: Generates synthetic animal data via an API.
- **ML Pipeline**: Handles data cleaning, visualization, clustering, and model training.
- **Backend (FastAPI)**: REST API to serve predictions from the trained model.
- **Frontend (Streamlit)**: Web dashboard for users to input data and receive predictions.
- **MinIO**: Object storage for saving and retrieving trained models.
- **Docker & Docker Compose**: Easy containerized deployment for all services.

## future improvements

- To prevent overwriting, databases and queries will be generated based on the creation date and the specific model used at that time. This approach will support multiple model versions and enable clients to access historical data.

## ⚙️ How to Run It

To launch the full application locally:

```bash
docker-compose build
docker-compose up

Note: The .env file is required for both the frontend and backend to correctly connect to the other services.

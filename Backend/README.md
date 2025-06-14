# Backend - Animal Classifier API

This backend service is responsible for the core functionality of the animal classifier system. It automates the following workflow:

1. Fetch data from a remote data service.
2. Clean and process the dataset.
3. Train a machine learning model.
4. Save the model to an object storage (MinIO).
5. Deploy a FastAPI service to serve predictions.

##  Running the Backend with Docker Only

If you want to run the backend independently without using Docker Compose, follow these steps:

### 1. Build the Docker image

From the root of the project, run:

```bash
docker build -t animal-backend -f Dockerfile .

docker run -p 8000:8000 animal-backend

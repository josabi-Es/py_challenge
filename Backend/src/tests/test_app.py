import pytest
from fastapi.testclient import TestClient
from my_api.app import app

client = TestClient(app)

@pytest.mark.parametrize("input_data, expected_label", [
    ([{"walks_on_n_legs": 2, "height": 1.7, "weight": 50, "has_wings": False, "has_tail": True}], ["Kangaroo"]),
    ([{"walks_on_n_legs": 4, "height": 3.0, "weight": 500, "has_wings": False, "has_tail": True}], ["Elephant"]),
    ([{"walks_on_n_legs": 4, "height": 0.5, "weight": 20, "has_wings": False, "has_tail": True}], ["Dog"]),
    ([{"walks_on_n_legs": 2, "height": 0.3, "weight": 2.5, "has_wings": True, "has_tail": True}], ["Chicken"]),
])
def test_predict_all_animals(monkeypatch, input_data, expected_label):
    class DummyModel:
        def predict(self, X):
            mapping = {"Kangaroo": 1, "Elephant": 2, "Dog": 3, "Chicken": 4}
            return [mapping[expected_label[0]]]

    # Ajusta aquí las rutas del monkeypatch para que coincidan con tu paquete my_api
    monkeypatch.setattr("my_api.DataPreprocessing_MachineLearning.get_model_minio", lambda _: DummyModel())
    monkeypatch.setattr("my_api.DataPreprocessing_MachineLearning.predict_train", lambda m, d: expected_label)

    response = client.post("/api/v1/predict", json=input_data)
    assert response.status_code == 200
    assert response.json() == expected_label

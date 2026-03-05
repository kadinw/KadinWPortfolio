from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/lab/health")
    assert response.status_code == 200


def test_predict_basic():
    data = {
        "MedInc": 1,
        "HouseAge": 1,
        "AveRooms": 3,
        "AveBedrms": 3,
        "Population": 3,
        "AveOccup": 5,
        "Latitude": 1,
        "Longitude": 1,
    }
    response = client.post(
        "/lab/predict",
        json=data,
    )
    assert response.status_code == 200
    assert isinstance(response.json()["prediction"], float)

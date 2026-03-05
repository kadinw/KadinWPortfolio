import pytest
from datetime import datetime

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root_returns_404():
    resp = client.get("/")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Not Found"}


def test_lab_health_ok_and_returns_time():
    resp = client.get("/lab/health")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/json")
    body = resp.json()
    assert "time" in body
    assert isinstance(body["time"], str)
    # Validate ISO8601 (datetime.fromisoformat accepts offsets like +00:00)
    datetime.fromisoformat(body["time"].replace("Z", "+00:00"))


@pytest.mark.parametrize(
    "name",
    [
        "Kadin",
        "x",
        "Kadin Wilkins",
        "O'Donnel",
        "John-Doe",
        "k" * 200,
    ],
)
def test_lab_hello_valid_names(name: str):
    resp = client.get("/lab/hello", params={"name": name})
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/json")
    assert resp.json() == {"message": f"Hello {name}"}


def test_lab_hello_missing_name_returns_error():
    resp = client.get("/lab/hello")
    assert resp.status_code == 422
    data = resp.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)
    err = data["detail"][0]
    assert err["loc"] == ["query", "name"]


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
    resp = client.post("/lab/predict", json=data)
    assert resp.status_code == 200
    assert isinstance(resp.json()["prediction"], float)


@pytest.mark.parametrize("bad_lat", [-90.0001, 90.0001, 999])
def test_predict_rejects_bad_latitude(bad_lat: float):
    data = {
        "MedInc": 1,
        "HouseAge": 1,
        "AveRooms": 3,
        "AveBedrms": 3,
        "Population": 3,
        "AveOccup": 5,
        "Latitude": bad_lat,
        "Longitude": 1,
    }
    resp = client.post("/lab/predict", json=data)
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert any("Value error, Invalid value for Latitude" in err.get("msg", "") for err in detail)


@pytest.mark.parametrize("bad_lon", [-180.0001, 180.0001, 999])
def test_predict_rejects_bad_longitude(bad_lon: float):
    data = {
        "MedInc": 1,
        "HouseAge": 1,
        "AveRooms": 3,
        "AveBedrms": 3,
        "Population": 3,
        "AveOccup": 5,
        "Latitude": 1,
        "Longitude": bad_lon,
    }
    resp = client.post("/lab/predict", json=data)
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert any("Value error, Invalid value for Longitude" in err.get("msg", "") for err in detail)


def test_unknown_route_returns_404():
    resp = client.get("/definitely-not-a-real-route")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Not Found"

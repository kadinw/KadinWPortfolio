import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_root_returns_404():
    resp = client.get("/")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Not Found"}


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/json")
    assert resp.json() == {"status": "healthy"}


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
def test_hello_valid_names(name: str):
    resp = client.get("/hello", params={"name": name})
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/json")
    assert resp.json() == {"message": f"Hello {name}"}


def test_hello_missing_name_returns_error():
    resp = client.get("/hello")
    assert resp.status_code == 422

    data = resp.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)

    err = data["detail"][0]
    assert err["loc"] == ["query", "name"]
    assert err["msg"] in ("Field required", "field required")


@pytest.mark.parametrize(
    "bad_name",
    [
        None,
        2,
        4.4,
        True,
        ["list"],
        {"obj": "value"},
    ],
)
def test_hello_rejects_non_string_types(bad_name):
    resp = client.get("/hello")
    assert resp.status_code == 422
    data = resp.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert any(
        err.get("loc") == ["query", "name"]
        for err in data["detail"]
    )


def test_openapi_json_is_accessible_and_has_expected_paths():
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/json")

    spec = resp.json()

    assert "openapi" in spec
    assert isinstance(spec["openapi"], str)
    assert spec["openapi"].startswith("3.")

    assert "paths" in spec
    paths = spec["paths"]

    assert "/" in paths
    assert "/health" in paths
    assert "/hello" in paths

def test_unknown_route_returns_404():
    resp = client.get("/definitely-not-a-real-route")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Not Found"

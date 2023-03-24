import requests
import pytest
from src.web import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_index_api(client):
    response = client.get("http://localhost:5000/api/club/disciplines/")
    assert response.status_code == 200

    data = response.get_json()["data"]
    assert len(data) == 7
    assert data[0]["name"] == "Futbol"
    assert data[0]["teacher"] == "Juan"
    assert data[0]["dates"] == "Lunes 6:00pm - 8:00pm"


def test_index_api_costs(client):
    response = client.get("http://localhost:5000/api/club/disciplines/disciplines_with_costs")
    assert response.status_code == 200
    data = response.get_json()["data"]


    assert len(data) == 7
    assert data[0]["name"] == "Futbol"
    assert data[0]["teacher"] == "Juan"
    assert data[0]["dates"] == "Lunes 6:00pm - 8:00pm"
    assert data[0]["monthly_cost"] in ["800.0", "800"]
    assert data[0]["category"] == "12 a 14 años"

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


def test_member_paymets_api(client):
    response = client.get("http://localhost:5000/api/me/payments/1")
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data) == 5
    assert data["name"] == "Juan"
    assert data["surname"] == "Perez"
    assert len(data["payments"]) == 1


def test_post_payments_api(app, client):
    response = client.get("http://localhost:5000/api/me/payments/1")
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data["payments"]) == 1
    client.post("http://localhost:5000/api/me/payments/1")

    response = client.get("http://localhost:5000/api/me/payments/1")
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data["payments"]) == 2
    with app.app_context():
        from src.core.board import delete_payment

        delete_payment(data["payments"][-1]["id"])

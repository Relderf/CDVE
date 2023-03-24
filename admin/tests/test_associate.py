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


@pytest.fixture()
def auth_user_with_disciplines(client):
    login = client.post(
        "/api/auth/login", json={"password": "1234", "username": "22583743"}
    )
    return (
        filter(
            lambda x: "access_token_cookie" in x, login.headers.get_all("Set-Cookie")
        )
        .__next__()
        .split(";")[0]
        .split("=")[1]
    )


@pytest.fixture()
def auth_user_empty(client):
    login = client.post(
        "/api/auth/login", json={"password": "1234", "username": "46583754"}
    )
    return (
        filter(
            lambda x: "access_token_cookie" in x, login.headers.get_all("Set-Cookie")
        )
        .__next__()
        .split(";")[0]
        .split("=")[1]
    )


def test_my_disciplines_without_credentials(client):
    response = client.get("/api/me/disciplines/")
    data = response.get_json()

    assert response.status_code == 401
    assert len(data) == 1
    assert data["msg"] != ""


def test_my_disciplines_with_credentials_with_data(client, auth_user_with_disciplines):
    response = client.get(
        "/api/me/disciplines/",
        headers={"Cookie": "access_token_cookie=" + auth_user_with_disciplines},
    )
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0].get("name") == "Futbol"


def test_my_disciplines_with_credentials_empty(client, auth_user_empty):
    response = client.get(
        "/api/me/disciplines/",
        headers={"Cookie": "access_token_cookie=" + auth_user_empty},
    )
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert len(data) == 0


def test_my_license_without_credentials(client):
    response = client.get("/api/me/license/")
    data = response.get_json()

    assert response.status_code == 401
    assert len(data) == 1
    assert data["msg"] != ""


def test_my_license_with_credentials(client, auth_user_with_disciplines):
    response = client.get(
        "/api/me/license/",
        headers={"Cookie": "access_token_cookie=" + auth_user_with_disciplines},
    )
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert len(data) == 8
    assert data.get("status") == "Moroso"
    assert data.get("surname") == "Perez"

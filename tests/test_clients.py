from fastapi.testclient import TestClient
from app.main import app


def test_create_client(client):

    client_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "09171234567",
        "address": "Manila, Philippines"
    }

    response = client.post("/clients", json=client_data)

    assert response.status_code==201

    data = response.json()

    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["phone"] == "09171234567"
    assert data["address"] == "Manila, Philippines"
    assert "id" in data


def test_create_client_duplicate_email(client):
    client_data = {
        "name": "John Doe",
        "email": "john@example.com",
    }

    first_response = client.post("/clients", json=client_data)
    second_response = client.post("/clients", json=client_data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_get_clients(client):

    client.post(
        "/clients",
        json={
            "name": "John Doe",
            "email": "john@sample.com"
        }
    )

    client.post(
        "/clients",
        json={
            "name": "Adam Eve",
            "email": "adam@sample.com"
        }
    )

    response = client.get("/clients")

    assert response.status_code==200
    assert len(response.json()) == 2


def test_get_clients_by_name(client):

    client.post("/clients", json={
        "name": "John Doe"
    })

    client.post("/clients", json={
        "name": "Adam Eve"
    })

    response = client.get("/clients", params={"name": "adam"})

    data = response.json()
    assert response.status_code==200
    assert len(data)==1
    assert data[0]["name"] == "Adam Eve"


def test_search_client_by_id(client):

    response = client.post("/clients", json={
        "name": "John Doe"
    })

    assert response.status_code==201

    client_id = response.json()["id"]

    get_response = client.get("/clients", params={"client_id": client_id})

    assert get_response.json()[0]["id"] == client_id
    assert get_response.status_code==200
    assert len(get_response.json()) == 1


def test_get_client_by_id(client):
    create_response = client.post("/clients", json={
        "name": "John Doe"
    })

    client_id = create_response.json()["id"]

    response = client.get(f"/clients/{client_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"


def test_get_client_not_found(client):
    response = client.get("/clients/9999")

    assert response.status_code == 404


def test_update_client(client):

    create_response = client.post("/clients", json={
        "name": "John Doe",
        "email": "john@sample.com"
    })

    assert create_response.status_code==201

    client_id = create_response.json()["id"]

    update_client = {
        "name": "John Doe",
        "email": "john@sample.com",
        "phone": "09171234567",
        "address": "Makati, Philippines"
    }

    update_response = client.put(f"/clients/{client_id}", json=update_client)

    assert update_response.status_code==200

    data = update_response.json()

    assert data["phone"] == "09171234567"
    assert data["address"] == "Makati, Philippines"

def test_delete_client(client):
    create_response = client.post("/clients", json={
        "name": "John Doe"
    })

    client_id = create_response.json()["id"]

    response = client.delete(f"/clients/{client_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/clients/{client_id}")

    assert get_response.status_code == 404


def test_delete_client_not_found(client):
    response = client.delete("/clients/9999")

    assert response.status_code == 404
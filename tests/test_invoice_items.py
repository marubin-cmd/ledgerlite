
import pytest

from app.models.client import Client
from app.models.invoice import Invoice


@pytest.fixture

def db_client(db_session):

    client = Client(
        name = "Test Client",
        email = "test@example.com",
        phone = "09123456789",
        address = "Manila, Philippines"
    )

    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)

    return client


def create_invoice(client, client_id):

    response = client.post(
        "/invoices",
        json = {
            "client_id": client_id,
            "type": "income",
            "issue_date": "2026-11-01",
            "due_date": "2026-11-30",
            "notes": "Test invoice"
        }
    )

    assert response.status_code==201, response.text

    return response.json()


def create_invoice_item(client, invoice_id, **overrides):

    payload = {
        "description": "Development service",
        "quantity": 2,
        "unit_price": "500.00"
    }

    payload.update(overrides)

    response = client.post(
        f"/invoices/{invoice_id}/items",
        json=payload
    )

    assert response.status_code==201, response.text

    return response.json()

# TEST CASES

def test_create_invoice_item(client, db_client):

    invoice = create_invoice(client, db_client.id)
    
    response = client.post(
        f"/invoices/{invoice["id"]}/items",
        json={
            "description": "Development service",
            "quantity": 2,
            "unit_price": "500.00"
        }
    )

    data = response.json()

    assert data["invoice_id"] == invoice["id"]
    assert data["description"] == "Development service"
    assert data["quantity"] == 2
    assert float(data["unit_price"]) == 500.00
    assert float(data["total"]) == 1000.00


def test_create_invoice_item_invalid_quantity(client, db_client):

    invoice = create_invoice(client, db_client.id)

    data = client.post(
        f"/invoices/{invoice["id"]}/items",
        json={
            "description": "Development service",
            "quantity": 0,
            "unit_price": "500.00"
        }
    )

    assert data.status_code==422



def test_create_invoice_item_decimal_quantity(client, db_client):

    invoice = create_invoice(client, db_client.id)

    data = client.post(
        f"/invoices/{invoice["id"]}/items",
        json={
            "description": "Development service",
            "quantity": 1.5,
            "unit_price": "500.00"
        }
    )

    assert data.status_code==422


def test_create_invoice_item_negative_price(client, db_client):

    invoice = create_invoice(client, db_client.id)

    data = client.post(
        f"/invoices/{invoice["id"]}/items",
        json={
            "description": "Development service",
            "quantity": 2,
            "unit_price": "-500.00"
        }
    )

    assert data.status_code==422


def test_create_invoice_item_invalid_decimal_places(client, db_client):

    invoice = create_invoice(client, db_client.id)

    data = client.post(
        f"/invoices/{invoice["id"]}/items",
        json={
            "description": "Development service",
            "quantity": 2,
            "unit_price": "500.9999"
        }
    )

    assert data.status_code==422


def test_create_invoice_item_invoice_not_found(client):

    data = client.post(
        "/invoices/999/items",
        json={
            "description": "Development service",
            "quantity": 2,
            "unit_price": "500.00"
        }
    )

    assert data.status_code==404
    assert data.json()["detail"] == "Invoice not found"

# GET INVOICE ITEMS

def test_get_invoice_items_success(client, db_client):
    invoice = create_invoice(client, db_client.id)

    create_invoice_item(client, invoice["id"])
    create_invoice_item(
        client,
        invoice["id"],
        description="Consultation",
        quantity=1,
        unit_price="300.00"
    )

    response = client.get(
        f"/invoices/{invoice['id']}/items"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["invoice_id"] == invoice["id"]


def test_get_invoice_items_empty(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.get(
        f"/invoices/{invoice['id']}/items"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_invoice_items_invoice_not_found(client):
    response = client.get("/invoices/9999/items")

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice not found"


# GET SINGLE INVOICE ITEM

def test_get_invoice_item_success(client, db_client):
    invoice = create_invoice(client, db_client.id)

    item = create_invoice_item(client, invoice["id"])

    response = client.get(
        f"/invoices/{invoice['id']}/items/{item['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == item["id"]
    assert response.json()["description"] == "Development service"


def test_get_invoice_item_not_found(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.get(
        f"/invoices/{invoice['id']}/items/9999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice item not found"


def test_get_invoice_item_wrong_invoice(client, db_client):
    invoice1 = create_invoice(client, db_client.id)
    invoice2 = create_invoice(client, db_client.id)

    item = create_invoice_item(client, invoice1["id"])

    response = client.get(
        f"/invoices/{invoice2['id']}/items/{item['id']}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice item not found"


# UPDATE INVOICE ITEM

def test_update_invoice_item_success(client, db_client):
    invoice = create_invoice(client, db_client.id)
    item = create_invoice_item(client, invoice["id"])

    response = client.patch(
        f"/invoices/{invoice['id']}/items/{item['id']}",
        json={
            "description": "Updated development service",
            "quantity": 3,
            "unit_price": "750.00"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == "Updated development service"
    assert data["quantity"] == 3
    assert float(data["unit_price"]) == 750.00
    assert float(data["total"]) == 2250.00


def test_update_invoice_item_partial_update(client, db_client):
    invoice = create_invoice(client, db_client.id)
    item = create_invoice_item(client, invoice["id"])

    response = client.patch(
        f"/invoices/{invoice['id']}/items/{item['id']}",
        json={
            "quantity": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["quantity"] == 5
    assert data["description"] == "Development service"
    assert float(data["unit_price"]) == 500.00
    assert float(data["total"]) == 2500.00


def test_update_invoice_item_invalid_quantity(client, db_client):
    invoice = create_invoice(client, db_client.id)
    item = create_invoice_item(client, invoice["id"])

    response = client.patch(
        f"/invoices/{invoice['id']}/items/{item['id']}",
        json={
            "quantity": 0
        }
    )

    assert response.status_code == 422


def test_update_invoice_item_null_description(client, db_client):
    invoice = create_invoice(client, db_client.id)
    item = create_invoice_item(client, invoice["id"])

    response = client.patch(
        f"/invoices/{invoice['id']}/items/{item['id']}",
        json={
            "description": None
        }
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "description cannot be NULL"


def test_update_invoice_item_not_found(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.patch(
        f"/invoices/{invoice['id']}/items/9999",
        json={
            "description": "Updated service"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice item not found"


def test_update_invoice_item_wrong_invoice(client, db_client):
    invoice1 = create_invoice(client, db_client.id)
    invoice2 = create_invoice(client, db_client.id)

    item = create_invoice_item(client, invoice1["id"])

    response = client.patch(
        f"/invoices/{invoice2['id']}/items/{item['id']}",
        json={
            "description": "Unauthorized update"
        }
    )

    assert response.status_code == 404


def test_update_invoice_item_non_draft_invoice(
    client,
    db_client,
    db_session
):
    invoice = create_invoice(client, db_client.id)
    item = create_invoice_item(client, invoice["id"])

    db_invoice = db_session.get(Invoice, invoice["id"])
    db_invoice.status = "paid"
    db_session.commit()

    response = client.patch(
        f"/invoices/{invoice['id']}/items/{item['id']}",
        json={
            "quantity": 5
        }
    )

    assert response.status_code == 409


# DELETE INVOICE ITEM

def test_delete_invoice_item_success(client, db_client):
    invoice = create_invoice(client, db_client.id)
    item = create_invoice_item(client, invoice["id"])

    response = client.delete(
        f"/invoices/{invoice['id']}/items/{item['id']}"
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(
        f"/invoices/{invoice['id']}/items/{item['id']}"
    )

    assert get_response.status_code == 404


def test_delete_invoice_item_not_found(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.delete(
        f"/invoices/{invoice['id']}/items/9999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice item not found"


def test_delete_invoice_item_wrong_invoice(client, db_client):
    invoice1 = create_invoice(client, db_client.id)
    invoice2 = create_invoice(client, db_client.id)

    item = create_invoice_item(client, invoice1["id"])

    response = client.delete(
        f"/invoices/{invoice2['id']}/items/{item['id']}"
    )

    assert response.status_code == 404


def test_delete_invoice_item_non_draft_invoice(
    client,
    db_client,
    db_session
):
    invoice = create_invoice(client, db_client.id)
    item = create_invoice_item(client, invoice["id"])

    db_invoice = db_session.get(Invoice, invoice["id"])
    db_invoice.status = "paid"
    db_session.commit()

    response = client.delete(
        f"/invoices/{invoice['id']}/items/{item['id']}"
    )

    assert response.status_code == 409


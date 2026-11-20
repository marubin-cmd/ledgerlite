
import pytest

from app.models.client import Client
from app.models.invoice import Invoice


@pytest.fixture
def db_client(db_session):
    client = Client(
        name="Test Client",
        email="test@example.com",
        phone="09123456789",
        address="Manila, Philippines"
    )

    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)

    return client


def create_invoice(client, client_id, **overrides):
    payload = {
        "client_id": client_id,
        "type": "income",
        "issue_date": "2026-11-01",
        "due_date": "2026-11-30",
        "notes": "Test invoice"
    }

    payload.update(overrides)

    response = client.post("/invoices", json=payload)

    assert response.status_code == 201, response.text

    return response.json()


# CREATE INVOICE

def test_create_invoice_success(client, db_client):
    response = client.post(
        "/invoices",
        json={
            "client_id": db_client.id,
            "type": "income",
            "issue_date": "2026-11-01",
            "due_date": "2026-11-30",
            "notes": "Monthly service"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["client_id"] == db_client.id
    assert data["type"] == "income"
    assert data["status"] == "draft"
    assert data["invoice_number"].startswith("INV-")
    assert data["notes"] == "Monthly service"


def test_create_invoice_client_not_found(client):
    response = client.post(
        "/invoices",
        json={
            "client_id": 9999,
            "type": "income",
            "issue_date": "2026-11-01",
            "due_date": "2026-11-30"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_create_invoice_invalid_dates(client, db_client):
    response = client.post(
        "/invoices",
        json={
            "client_id": db_client.id,
            "type": "income",
            "issue_date": "2026-11-30",
            "due_date": "2026-11-01"
        }
    )

    assert response.status_code == 422


def test_create_invoice_invalid_type(client, db_client):
    response = client.post(
        "/invoices",
        json={
            "client_id": db_client.id,
            "type": "invalid",
            "issue_date": "2026-11-01",
            "due_date": "2026-11-30"
        }
    )

    assert response.status_code == 422


# GET INVOICES

def test_get_invoices_empty(client):
    response = client.get("/invoices")

    assert response.status_code == 200
    assert response.json() == []


def test_get_invoices_success(client, db_client):
    create_invoice(client, db_client.id)
    create_invoice(client, db_client.id, type="expense")

    response = client.get("/invoices")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_invoices_filter_by_type(client, db_client):
    create_invoice(client, db_client.id, type="income")
    create_invoice(client, db_client.id, type="expense")

    response = client.get("/invoices?invoice_type=income")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["type"] == "income"


def test_get_invoices_filter_by_status(client, db_client, db_session):
    invoice = create_invoice(client, db_client.id)

    db_invoice = db_session.get(Invoice, invoice["id"])
    db_invoice.status = "paid"
    db_session.commit()

    response = client.get("/invoices?invoice_status=paid")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "paid"


def test_get_invoices_pagination(client, db_client):
    create_invoice(client, db_client.id)
    create_invoice(client, db_client.id)
    create_invoice(client, db_client.id)

    response = client.get("/invoices?limit=2&offset=1")

    assert response.status_code == 200
    assert len(response.json()) == 2


# GET INVOICE BY ID

def test_get_invoice_by_id_success(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.get(f"/invoices/{invoice['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == invoice["id"]


def test_get_invoice_by_id_not_found(client):
    response = client.get("/invoices/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice not found"


# UPDATE INVOICE

def test_update_invoice_success(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.patch(
        f"/invoices/{invoice['id']}",
        json={
            "notes": "Updated invoice notes"
        }
    )

    assert response.status_code == 200
    assert response.json()["notes"] == "Updated invoice notes"


def test_update_invoice_not_found(client):
    response = client.patch(
        "/invoices/9999",
        json={"notes": "Updated notes"}
    )

    assert response.status_code == 404


def test_update_invoice_invalid_dates(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.patch(
        f"/invoices/{invoice['id']}",
        json={
            "due_date": "2026-10-01"
        }
    )

    assert response.status_code == 422


def test_update_invoice_null_required_field(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.patch(
        f"/invoices/{invoice['id']}",
        json={
            "issue_date": None
        }
    )

    assert response.status_code == 422


def test_update_invoice_client_not_found(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.patch(
        f"/invoices/{invoice['id']}",
        json={
            "client_id": 9999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


# CANCEL INVOICE

def test_cancel_invoice_success(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.post(
        f"/invoices/{invoice['id']}/cancel"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


def test_cancel_invoice_already_cancelled(client, db_client):
    invoice = create_invoice(client, db_client.id)

    client.post(f"/invoices/{invoice['id']}/cancel")

    response = client.post(
        f"/invoices/{invoice['id']}/cancel"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Invoice is already cancelled"


@pytest.mark.parametrize(
    "invoice_status",
    ["paid", "partially_paid", "overdue"]
)
def test_cancel_invoice_unsupported_status(
    client,
    db_client,
    db_session,
    invoice_status
):
    invoice = create_invoice(client, db_client.id)

    db_invoice = db_session.get(Invoice, invoice["id"])
    db_invoice.status = invoice_status
    db_session.commit()

    response = client.post(
        f"/invoices/{invoice['id']}/cancel"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Only draft or unpaid invoices can be cancelled"
    )


def test_cancel_invoice_not_found(client):
    response = client.post("/invoices/9999/cancel")

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice not found"


def test_issue_invoice_success(client, db_client):
    invoice = create_invoice(client, db_client.id)

    client.post(
        f"/invoices/{invoice['id']}/items",
        json={
            "description": "Development service",
            "quantity": 2,
            "unit_price": "500.00"
        }
    )

    response = client.post(
        f"/invoices/{invoice['id']}/issue"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "unpaid"
    assert response.json()["subtotal"] == "1000.00"


def test_issue_invoice_without_items(client, db_client):
    invoice = create_invoice(client, db_client.id)

    response = client.post(
        f"/invoices/{invoice['id']}/issue"
    )

    assert response.status_code == 409


def test_issue_invoice_not_found(client):
    response = client.post("/invoices/9999/issue")

    assert response.status_code == 404

def test_issue_invoice_already_issued(client, db_client):
    invoice = create_invoice(client, db_client.id)

    client.post(
        f"/invoices/{invoice['id']}/items",
        json={
            "description": "Development service",
            "quantity": 1,
            "unit_price": "500.00"
        }
    )

    first = client.post(
        f"/invoices/{invoice['id']}/issue"
    )

    second = client.post(
        f"/invoices/{invoice['id']}/issue"
    )

    assert first.status_code == 200
    assert second.status_code == 409


def test_issue_cancelled_invoice(client, db_client):
    invoice = create_invoice(client, db_client.id)

    client.post(
        f"/invoices/{invoice['id']}/cancel"
    )

    response = client.post(
        f"/invoices/{invoice['id']}/issue"
    )

    assert response.status_code == 409
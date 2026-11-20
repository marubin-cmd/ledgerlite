from app.models.client import Client
from datetime import date
from decimal import Decimal

from app.models.transaction import Transaction

def create_test_client(db_session, name="Test Client", email="test@example.com"):

    test_client = Client(
        name=name,
        email=email,
        phone="09123456789",
        address="Manila, Philippines"
    )

    db_session.add(test_client)
    db_session.commit()
    db_session.refresh(test_client)

    return test_client


def create_invoice(client, client_id, total=None, issue=False, invoice_type="income"):

    invoice_response = client.post(
        "/invoices",
        json={
            "client_id": client_id,
            "type": invoice_type,
            "issue_date": "2026-11-19",
            "due_date": "2026-11-30"
        }
    )

    assert invoice_response.status_code == 201, invoice_response.text


    invoice_id = invoice_response.json()["id"]


    # Add an invoice item if a total was provided.
    if total is not None:
        item_response = client.post(
            f"/invoices/{invoice_id}/items",
            json={
                "description": "IT Services",
                "quantity": 1,
                "unit_price": str(total)
            }
        )
        assert item_response.status_code == 201, item_response.text

    if issue:

        issue_response = client.post(
            f"/invoices/{invoice_id}/issue"
        )

        assert issue_response.status_code == 200, issue_response.text


    return invoice_id



def test_create_payment_success(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    payment_data = payment_response.json()

    assert payment_data["invoice_id"] == invoice_id
    assert payment_data["amount"] == "600.00"
    assert payment_data["payment_method"] == "cash"


# Verify that a transaction was automatically created.
    transaction = (
        db_session.query(Transaction)
        .filter(Transaction.payment_id == payment_data["id"])
        .first()
    )

    assert transaction is not None
    assert transaction.amount == Decimal("600.00")
    assert transaction.transaction_type == "income"
    assert transaction.transaction_date == date(2026, 11, 19)
    assert transaction.description.startswith("Payment for ")
    assert transaction.payment_id == payment_data["id"]

    
    invoice = client.get(
        f"/invoices/{invoice_id}"
    ).json()

    assert invoice["subtotal"] == "1600.00"
    assert invoice["total"] == "1600.00"
    assert invoice["amount_paid"] == "600.00"
    assert invoice["balance"] == "1000.00"
    assert invoice["status"] == "partially_paid"




def test_create_payment_exceeds_balance(client, db_session):
    test_client = create_test_client(
        db_session,
        name="Overpayment Test Client",
        email="overpayment@example.com"
    )

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    first_payment = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert first_payment.status_code == 201

    second_payment = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "1200.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert second_payment.status_code == 422

    invoice = client.get(f"/invoices/{invoice_id}").json()

    assert invoice["amount_paid"] == "600.00"
    assert invoice["balance"] == "1000.00"
    assert invoice["status"] == "partially_paid"



def test_create_payment_draft_invoice(client, db_session):
    test_client = create_test_client(db_session)

    # Create an invoice but leave it as draft.
    invoice_id = create_invoice(
        client,
        test_client.id
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "500.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 409
    assert payment_response.json()["detail"] == (
        "Payments can only be recorded for unpaid or partially paid invoices"
    )



def test_get_payments(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="2000.00",
        issue=True
    )

    # Record two payments
    first_payment = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "500.00",
            "payment_date": "2026-11-18",
            "payment_method": "cash"
        }
    )

    second_payment = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "700.00",
            "payment_date": "2026-11-19",
            "payment_method": "bank_transfer"
        }
    )

    assert first_payment.status_code == 201
    assert second_payment.status_code == 201

    # Retrieve payment history
    response = client.get(
        f"/invoices/{invoice_id}/payments"
    )

    assert response.status_code == 200

    payments = response.json()

    assert len(payments) == 2
    assert payments[0]["amount"] == "700.00"
    assert payments[1]["amount"] == "500.00"



def test_get_payment(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    payment_id = payment_response.json()["id"]

    response = client.get(
        f"/invoices/{invoice_id}/payments/{payment_id}"
    )

    assert response.status_code == 200

    payment_data = response.json()

    assert payment_data["id"] == payment_id
    assert payment_data["invoice_id"] == invoice_id
    assert payment_data["amount"] == "600.00"
    assert payment_data["payment_method"] == "cash"



def test_get_payment_not_found(client, db_session):

    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client, 
        test_client.id, 
        total="1500.00",
        issue=True
    )

    response = client.get(
        f"/invoices/{invoice_id}/payments/9999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"



def test_get_payment_invoice_not_found(client):
    response = client.get(
        "/invoices/99999/payments/1"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice not found"



def test_update_payment_success(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="2000.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "500.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    payment_id = payment_response.json()["id"]

    response = client.patch(
        f"/invoices/{invoice_id}/payments/{payment_id}",
        json={
            "amount": "800.00",
            "payment_method": "bank_transfer"
        }
    )

    assert response.status_code == 200

    payment_data = response.json()

    assert payment_data["id"] == payment_id
    assert payment_data["amount"] == "800.00"
    assert payment_data["payment_method"] == "bank_transfer"

    invoice = client.get(
        f"/invoices/{invoice_id}"
    ).json()

    assert invoice["amount_paid"] == "800.00"
    assert invoice["balance"] == "1200.00"
    assert invoice["status"] == "partially_paid"

    transaction = (
    db_session.query(Transaction)
    .filter(Transaction.payment_id == payment_id)
    .first()
    )

    assert transaction is not None
    assert transaction.amount == Decimal("800.00")
    assert transaction.transaction_date == date(2026, 11, 19)
    assert transaction.payment_id == payment_id



def test_update_payment_exceeds_balance(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="2000.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "500.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    payment_id = payment_response.json()["id"]

    response = client.patch(
        f"/invoices/{invoice_id}/payments/{payment_id}",
        json={
            "amount": "2500.00"
        }
    )

    assert response.status_code == 422

    # Verify the original payment was not changed.
    payment = client.get(
        f"/invoices/{invoice_id}/payments/{payment_id}"
    ).json()

    assert payment["amount"] == "500.00"

    # Verify the invoice totals remain unchanged.
    invoice = client.get(
        f"/invoices/{invoice_id}"
    ).json()

    assert invoice["amount_paid"] == "500.00"
    assert invoice["balance"] == "1500.00"
    assert invoice["status"] == "partially_paid"



def test_update_payment_not_found(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    response = client.patch(
        f"/invoices/{invoice_id}/payments/99999",
        json={
            "amount": "500.00"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"



def test_delete_payment_success(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="2000.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "800.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    payment_id = payment_response.json()["id"]

    transaction = (
        db_session.query(Transaction)
        .filter(Transaction.payment_id == payment_id)
        .first()
    )

    assert transaction is not None

    response = client.delete(
        f"/invoices/{invoice_id}/payments/{payment_id}"
    )

    assert response.status_code == 204

    transaction = (
        db_session.query(Transaction)
        .filter(Transaction.payment_id == payment_id)
        .first()
    )

    assert transaction is None

    # Verify the payment was deleted.
    payment = client.get(
        f"/invoices/{invoice_id}/payments/{payment_id}"
    )

    assert payment.status_code == 404

    # Verify the invoice was recalculated.
    invoice = client.get(
        f"/invoices/{invoice_id}"
    ).json()

    assert invoice["amount_paid"] == "0.00"
    assert invoice["balance"] == "2000.00"
    assert invoice["status"] == "unpaid"



def test_delete_payment_not_found(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    response = client.delete(
        f"/invoices/{invoice_id}/payments/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


def test_update_payment_empty_payload(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    payment_id = payment_response.json()["id"]

    response = client.patch(
        f"/invoices/{invoice_id}/payments/{payment_id}",
        json={}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No fields provided for update"



def test_update_payment_amount_null(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    payment_id = payment_response.json()["id"]

    response = client.patch(
        f"/invoices/{invoice_id}/payments/{payment_id}",
        json={
            "amount": None
        }
    )

    assert response.status_code == 422

    payment = client.get(
        f"/invoices/{invoice_id}/payments/{payment_id}"
    ).json()

    assert payment["amount"] == "600.00"



def test_update_payment_date_null(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201
    payment_id = payment_response.json()["id"]

    response = client.patch(
        f"/invoices/{invoice_id}/payments/{payment_id}",
        json={"payment_date": None}
    )

    assert response.status_code == 422


def test_update_payment_method_null(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201
    payment_id = payment_response.json()["id"]

    response = client.patch(
        f"/invoices/{invoice_id}/payments/{payment_id}",
        json={"payment_method": None}
    )

    assert response.status_code == 422



def test_create_payment_invalid_method(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "500.00",
            "payment_date": "2026-11-19",
            "payment_method": "credit_card"
        }
    )

    assert response.status_code == 422


def test_create_payment_zero_amount(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "0.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert response.status_code == 422



def test_create_payment_negative_amount(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "-500.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert response.status_code == 422


def test_create_payment_exceeds_max_digits(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "100000000.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert response.status_code == 422



def test_create_payment_exceeds_decimal_places(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "500.255",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert response.status_code == 422



def test_update_payment_invalid_method(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="1600.00",
        issue=True
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-19",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    payment_id = payment_response.json()["id"]

    response = client.patch(
        f"/invoices/{invoice_id}/payments/{payment_id}",
        json={
            "payment_method": "credit_card"
        }
    )

    assert response.status_code == 422

    # Verify the original method remains unchanged.
    payment = client.get(
        f"/invoices/{invoice_id}/payments/{payment_id}"
    ).json()

    assert payment["payment_method"] == "cash"


def test_update_payment_invoice_not_found(client):
    response = client.patch(
        "/invoices/99999/payments/1",
        json={
            "amount": "500.00"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice not found"

def test_create_payment_expense_invoice(client, db_session):
    test_client = create_test_client(db_session)

    invoice_id = create_invoice(
        client,
        test_client.id,
        total="2000.00",
        issue=True,
        invoice_type="expense"
    )

    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-20",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    payment_id = payment_response.json()["id"]

    transaction = (
        db_session.query(Transaction)
        .filter(Transaction.payment_id == payment_id)
        .first()
    )

    assert transaction is not None
    assert transaction.amount == Decimal("600.00")
    assert transaction.transaction_type == "expense"
    assert transaction.transaction_date == date(2026, 11, 20)
    assert transaction.payment_id == payment_id
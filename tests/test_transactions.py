from fastapi.testclient import TestClient
from app.main import app
from app.models.transaction import Transaction

def test_create_transaction(client):

    transaction_data = {
            # description: str = Field(min_length=1, max_length=255)
            # amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
            # transaction_type: Literal["income", "expense"]
            # transaction_date: date

            "description": "Pytest test transaction",
            "amount": "123.50",
            "transaction_type": "income",
            "transaction_date": "2026-10-22"
    }

    response = client.post(
        "/transactions",
        json=transaction_data)

    assert response.status_code == 201

    data = response.json()

    assert data["description"] == "Pytest test transaction"
    assert data["amount"] == "123.50"
    assert data["transaction_type"] == "income"
    assert data["transaction_date"] == "2026-10-22"
    assert "id" in data

def test_filter_transactions_by_type(client):

    expense_data = {
        "description": "Test expense",
        "amount": "50.00",
        "transaction_type": "expense",
        "transaction_date": "2026-10-26"
    }

    income_data = {
        "description": "Test income",
        "amount": "500.00",
        "transaction_type": "income",
        "transaction_date": "2026-10-26"
    }

    expense_response = client.post(
        "/transactions",
        json=expense_data)

    income_response = client.post(
        "/transactions",
        json=income_data)

    assert expense_response.status_code == 201
    assert income_response.status_code == 201


    response = client.get(
        "/transactions",
        params={"transaction_type": "expense"},
    )

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) >= 1
    assert all(
        transaction["transaction_type"] == "expense"
        for transaction in transactions
    )
    assert any(
        transaction["description"] == "Test expense"
        for transaction in transactions
    )

def test_update_transaction(client):
     
    transaction_data = {
            "description": "Original description",
            "amount": "100.00",
            "transaction_type": "income",
            "transaction_date": "2026-10-26"
        }

    create_response = client.post(
        "/transactions",
        json=transaction_data
    )

    assert create_response.status_code==201

    updated_data = {
                "description": "Updated description",
                "amount": "100.00",
                "transaction_type": "income",
                "transaction_date": "2026-10-26"
            }

    transaction_id = create_response.json()["id"]

    update_response = client.put(
        f"/transactions/{transaction_id}",
        json=updated_data
    )

    assert update_response.status_code==200

    updated_transaction = update_response.json()
    assert updated_transaction["description"] == "Updated description"
    assert updated_transaction["amount"] == "100.00"
    assert updated_transaction["transaction_type"] == "income"


def test_delete_transaction(client):

    transaction_data = {
            "description": "Transaction to delete",
            "amount": "75.00",
            "transaction_type": "expense",
            "transaction_date": "2026-10-27",
        }

    create_transaction = client.post(
        "/transactions",
        json=transaction_data
    )

    assert create_transaction.status_code==201

    transaction_id = create_transaction.json()["id"]

    delete_response = client.delete(
        f"/transactions/{transaction_id}"
    )

    assert delete_response.status_code==204

    get_response = client.get(
        "/transactions",
        params={"transaction_type": "expense"}
    )

    assert get_response.status_code==200

    remaining_ids = [
        transaction["id"]
        for transaction in get_response.json()
    ]

    assert transaction_id not in remaining_ids


def test_transaction_summary(client):

   
    before_response = client.get("/transactions/summary")
    assert before_response.status_code == 200
    before = before_response.json()

   
    income_data = {
        "description": "Summary test income",
        "amount": "1234.50",
        "transaction_type": "income",
        "transaction_date": "2026-10-27",
    }

    expense_data = {
        "description": "Summary test expense",
        "amount": "234.50",
        "transaction_type": "expense",
        "transaction_date": "2026-10-27",
    }

    income_response = client.post("/transactions", json=income_data)
    expense_response = client.post("/transactions", json=expense_data)

    assert income_response.status_code == 201
    assert expense_response.status_code == 201

    after_response = client.get("/transactions/summary")
    assert after_response.status_code == 200
    after = after_response.json()

    assert round(float(after["total_income"]) - float(before["total_income"]), 2) == 1234.50
    assert round(float(after["total_expenses"]) - float(before["total_expenses"]), 2) == 234.50
    assert round(float(after["balance"]) - float(before["balance"]), 2) == 1000.00


def test_create_invalid_transaction(client):

    transaction_data = {
        "description": "Invalid transaction",
        "amount": "-100.00",
        "transaction_type": "expense",
        "transaction_date": "2026-10-28"
    }

    reponse = client.post(
        "/transactions",
        json=transaction_data
    )

    assert reponse.status_code==422

def test_update_nonexistent_transaction(client):

    updated_transaction = {
        "description": "Updated transaction",
        "amount": "200.00",
        "transaction_type": "expense",
        "transaction_date": "2026-10-28"
    }

    response = client.put(
        "/transactions/9999",
        json=updated_transaction
    )

    assert response.status_code==404


def test_delete_nonexistent_transaction(client):
    response = client.delete("/transactions/999999")

    assert response.status_code == 404

def test_transaction_pagination(client):
    # Create three transactions
    for i in range(3):
        transaction_data = {
            "description": f"Pagination test {i}",
            "amount": "100.00",
            "transaction_type": "income",
            "transaction_date": "2026-10-27",
        }

        response = client.post("/transactions", json=transaction_data)
        assert response.status_code == 201

    # Request the first two transactions
    first_page = client.get(
        "/transactions",
        params={"skip": 0, "limit": 2},
    )

    assert first_page.status_code == 200
    assert len(first_page.json()) == 2

    # Skip the first two transactions and request the next two
    second_page = client.get(
        "/transactions",
        params={"skip": 2, "limit": 2},
    )

    assert second_page.status_code == 200
    assert len(second_page.json()) == 1

def test_create_transaction_with_category(client):

    category_response = client.post(
        "/categories",
        json={
            "name": "Food",
            "description": "Meal and Groceries",
            "category_type": "expense"
        }
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    transaction_data = {
            "description": "Lunch",
            "amount": 250,
            "transaction_type": "expense",
            "transaction_date": "2026-11-03",
            "category_id": category_id,
    }

    transaction_response = client.post(
        "/transactions",
        json=transaction_data
    )

    assert transaction_response.status_code==201

    data = transaction_response.json()

    assert data["description"] == "Lunch"
    assert data["category_id"] == category_id

def test_create_transaction_without_category(client):

    transaction_data = {
                "description": "Coffee",
                "amount": 100,
                "transaction_type": "expense",
                "transaction_date": "2026-11-03",
        }

    transaction_response = client.post(
        "/transactions",
        json=transaction_data
    )

    assert transaction_response.status_code==201

    data = transaction_response.json()

    assert data["description"] == "Coffee"
    assert data["category_id"] is None


def test_create_transaction_with_invalid_category(client):

    transaction_data = {
        "description": "Dinner",
        "amount": 350,
        "transaction_type": "expense",
        "transaction_date": "2026-11-03",
        "category_id": 9999,
    }

    response = client.post(
        "/transactions",
        json=transaction_data,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}

def test_create_transaction_with_mismatched_category_type(client):

    category_response = client.post(
        "/categories",
        json={
            "name": "Food",
            "description": "Meal and Groceries",
            "category_type": "expense"
        }
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]


    transaction_data = {
            "description": "Dinner",
            "amount": 350,
            "transaction_type": "income",
            "transaction_date": "2026-11-03",
            "category_id": category_id
        }

    transaction_response = client.post(
        "/transactions",
        json=transaction_data
    )

    assert transaction_response.status_code==400
    assert transaction_response.json() == {"detail": "Category type must match transaction type"}

def test_update_transaction_with_mismatched_category_type(client):
    category_response = client.post(
        "/categories/",
        json={
            "name": "Salary",
            "description": "Monthly salary",
            "category_type": "income",
        },
    )

    category_id = category_response.json()["id"]
    assert category_response.status_code == 201

    transaction_response = client.post(
        "/transactions",
        json={
            "description": "Lunch",
            "amount": 250,
            "transaction_type": "expense",
            "transaction_date": "2026-11-03",
        },
    )

    transaction_id = transaction_response.json()["id"]

    updated_data = {
        "description": "Lunch",
        "amount": 250,
        "transaction_type": "expense",
        "transaction_date": "2026-11-03",
        "category_id": category_id,
    }

    response = client.put(
        f"/transactions/{transaction_id}",
        json=updated_data,
    )
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Category type must match transaction type"
    }

def test_delete_payment_linked_transaction(client, db_session):

    # Create a client.
    client_response = client.post(
        "/clients",
        json={
            "name": "Test Client",
            "email": "payment_test@example.com",
            "phone": "09123456789",
            "address": "Manila, Philippines"
        }
    )

    assert client_response.status_code == 201

    client_id = client_response.json()["id"]


    # Create an expense invoice.
    invoice_response = client.post(
        "/invoices",
        json={
            "client_id": client_id,
            "type": "expense",
            "issue_date": "2026-11-20",
            "due_date": "2026-11-30"
        }
    )

    assert invoice_response.status_code == 201

    invoice_id = invoice_response.json()["id"]  

    # Add an invoice item.
    item_response = client.post(
        f"/invoices/{invoice_id}/items",
        json={
            "description": "Office supplies",
            "quantity": 1,
            "unit_price": "2000.00"
        }
    )

    assert item_response.status_code == 201

    # Issue the invoice.
    issue_response = client.post(
        f"/invoices/{invoice_id}/issue"
    )

    assert issue_response.status_code == 200


    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "600.00",
            "payment_date": "2026-11-20",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code==201

    payment_id = payment_response.json()["id"]

    transaction = (
        db_session.query(Transaction)
        .filter(Transaction.payment_id == payment_id)
        .first()
    )

    assert transaction is not None

    # Attempt to delete the payment-linked transaction directly.
    response = client.delete(
        f"/transactions/{transaction.id}"
    )

    assert response.status_code == 409

    assert response.json()["detail"] == (
        "This transaction is linked to a payment. Delete the payment instead."
    )

    db_session.expire_all()

    transaction = db_session.get(Transaction, transaction.id)

    assert transaction is not None


def test_transaction_summary_includes_payment_transactions(client):

    # Create a client.
    client_response = client.post(
        "/clients",
        json={
            "name": "Summary Test Client",
            "email": "summary_test@example.com",
            "phone": "09123456789",
            "address": "Manila, Philippines"
        }
    )

    assert client_response.status_code == 201
    client_id = client_response.json()["id"]

    # Create an income invoice.
    invoice_response = client.post(
        "/invoices",
        json={
            "client_id": client_id,
            "type": "income",
            "issue_date": "2026-11-20",
            "due_date": "2026-12-20"
        }
    )

    assert invoice_response.status_code == 201
    invoice_id = invoice_response.json()["id"]

    # Add an invoice item worth 1000.
    item_response = client.post(
        f"/invoices/{invoice_id}/items",
        json={
            "description": "Summary test service",
            "quantity": 1,
            "unit_price": "1000.00"
        }
    )

    assert item_response.status_code == 201

    # Issue the invoice.
    issue_response = client.post(
        f"/invoices/{invoice_id}/issue"
    )

    assert issue_response.status_code == 200

    # Record a payment worth 300.
    payment_response = client.post(
        f"/invoices/{invoice_id}/payments",
        json={
            "amount": "300.00",
            "payment_date": "2026-11-20",
            "payment_method": "cash"
        }
    )

    assert payment_response.status_code == 201

    # Check the transaction summary.
    summary_response = client.get("/transactions/summary")

    assert summary_response.status_code == 200

    summary = summary_response.json()

    assert float(summary["total_income"]) == 300.00
    assert float(summary["total_expenses"]) == 0.00
    assert float(summary["balance"]) == 300.00
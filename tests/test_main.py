from fastapi.testclient import TestClient
from app.main import app



def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "database" in data


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


from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "database": "connected",
    }


def test_create_transaction():

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

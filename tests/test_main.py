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



def test_create_category(client):

    category_data = {
        "name": "Food",
        "description": "Dinner, Breakfast, Lunch, Restaurants, etc",
        "category_type": "expense"
    }


    response = client.post(
        "/categories",
        json=category_data
    )
   
    assert response.status_code == 201



def test_get_category(client):

    category_expense = {
            "name": "Food",
            "description": "Dinner, Breakfast, Lunch, Restaurants, etc",
            "category_type": "expense"
        }

    category_income = {
            "name": "Salary",
            "description": "Work, Freelance, Business",
            "category_type": "income"
        }


    response_expense = client.post(
        "/categories",
        json=category_expense
    )

    response_income = client.post(
        "/categories",
        json=category_income
    )

    assert response_expense.status_code == 201
    assert response_income.status_code == 201

    get_expense = client.get(
        "/categories",
        params={"category_type": "expense"}
    )

    get_income = client.get(
        "/categories",
        params={"category_type": "income"}
        )

    expense_data = get_expense.json()
    income_data = get_income.json()

    assert get_expense.status_code == 200
    assert get_income.status_code == 200

    assert all(
        category["category_type"] == "expense"
        for category in expense_data
    )

    assert all(
        category["category_type"] == "income"
        for category in income_data
    )


def test_update_category(client):

    category_data = {
        "name": "Food",
        "description": "Dinner, Breakfast, Lunch, Restaurants, etc",
        "category_type": "expense"
    }

    create_response = client.post(
        "/categories",
        json=category_data
    )     

    assert create_response.status_code == 201

    #UPDATE THE DATA

    updated_data = {
        "name": "Groceries",
        "description": "Food Supplies, Household materials",
        "category_type": "expense"
    }

    #GET THE CATEGORY ID

    category_id = create_response.json()["id"]

    #UPDATE THE CATEGORY

    update_response = client.put(
        f"/categories/{category_id}",
        json=updated_data
    )

    updated_category = update_response.json()

    assert update_response.status_code == 200

    assert updated_category["id"] == category_id
    assert updated_category["name"] == "Groceries"
    assert updated_category["description"] == "Food Supplies, Household materials"
    assert updated_category["category_type"] == "expense"



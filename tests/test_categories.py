from fastapi.testclient import TestClient
from app.main import app

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


def test_update_category_not_found(client):
    updated_data = {
        "name": "Groceries",
        "description": "Food and household supplies",
        "category_type": "expense",
    }

    response = client.put(
        "/categories/9999",
        json=updated_data,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Category not found"
    }

def test_delete_category(client):

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

    category_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/categories/{category_id}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get("/categories/")
    
    assert all(
        category["id"] != category_id
        for category in get_response.json()
    )

def test_delete_category_not_found(client):

    response = client.delete(
        "/categories/9999"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Category not found"
    }

def test_delete_category_with_assigned_transactions(client):
    category_response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "description": "Meals and groceries",
            "category_type": "expense",
        },
    )

    category_id = category_response.json()["id"]

    transaction_response = client.post(
        "/transactions",
        json={
            "description": "Lunch",
            "amount": 250,
            "transaction_type": "expense",
            "transaction_date": "2026-11-03",
            "category_id": category_id,
        },
    )

    assert transaction_response.status_code == 201

    response = client.delete(f"/categories/{category_id}")

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Cannot delete category because transactions are assigned to it"
    }
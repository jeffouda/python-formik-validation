import pytest
from app import app, db
from models import Customer


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_get_customers_empty(client):
    """Test GET /customers with no customers"""
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.get_json() == []


def test_post_customer(client):
    """Test POST /customers"""
    data = {"name": "John Doe", "email": "john@example.com", "age": 30}
    response = client.post("/customers", json=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["name"] == "John Doe"
    assert json_data["email"] == "john@example.com"
    assert json_data["age"] == 30
    assert "id" in json_data


def test_get_customers_after_post(client):
    """Test GET /customers after posting a customer"""
    data = {"name": "Jane Doe", "email": "jane@example.com", "age": 25}
    client.post("/customers", json=data)
    response = client.get("/customers")
    assert response.status_code == 200
    customers = response.get_json()
    assert len(customers) == 1
    assert customers[0]["name"] == "Jane Doe"
    assert customers[0]["email"] == "jane@example.com"
    assert customers[0]["age"] == 25

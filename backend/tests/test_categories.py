from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models

def test_create_category(test_client: TestClient, db_session: Session):
    response = test_client.post(
        "/api/v1/categories/",
        json={"name": "Electronics", "code": "ELEC"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Electronics"
    assert "id" in data

def test_read_categories(test_client: TestClient, db_session: Session):
    category1 = models.Category(name="Books", code="BKS")
    category2 = models.Category(name="Clothing", code="CLTH")
    db_session.add_all([category1, category2])
    db_session.commit()

    response = test_client.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert "Books" in [cat["name"] for cat in data]
    assert "Clothing" in [cat["name"] for cat in data]

def test_read_category(test_client: TestClient, db_session: Session):
    category = models.Category(name="Home Goods", code="HOME")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = test_client.get(f"/api/v1/categories/{category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Home Goods"
    assert data["id"] == category.id

def test_update_category(test_client: TestClient, db_session: Session):
    category = models.Category(name="Sports", code="SPRT")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    update_data = {"name": "Sports & Outdoors", "code": "SPRT-OUT"}
    response = test_client.put(
        f"/api/v1/categories/{category.id}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sports & Outdoors"
    assert data["code"] == "SPRT-OUT"

def test_delete_category(test_client: TestClient, db_session: Session):
    category = models.Category(name="Toys", code="TOY")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = test_client.delete(f"/api/v1/categories/{category.id}")
    assert response.status_code == 204

    # Verify that the category is deleted
    response = test_client.get(f"/api/v1/categories/{category.id}")
    assert response.status_code == 404

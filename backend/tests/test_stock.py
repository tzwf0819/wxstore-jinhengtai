from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models

def test_stock_in(test_client: TestClient, db_session: Session):
    # Create a product with initial stock
    product = models.Product(name="Stock In Product", price=10.0, stock=50)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = test_client.post(
        "/api/v1/stock/in",
        json={"product_id": product.id, "quantity": 25, "reference_id": "PO-123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product.id
    assert data["quantity"] == 25
    assert data["movement_type"] == "stock_in"

    # Verify product stock is updated by re-fetching it from the DB
    updated_product = db_session.get(models.Product, product.id)
    assert updated_product.stock == 75

def test_stock_out_return(test_client: TestClient, db_session: Session):
    product = models.Product(name="Stock Out Product", price=20.0, stock=100)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = test_client.post(
        "/api/v1/stock/out-return",
        json={"product_id": product.id, "quantity": 30, "reference_id": "RMA-456"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product.id
    assert data["quantity"] == 30
    assert data["movement_type"] == "stock_out_return"

    # Verify product stock is updated by re-fetching it
    db_session.commit()
    updated_product = db_session.get(models.Product, product.id)
    assert updated_product.stock == 70

def test_stock_out_insufficient(test_client: TestClient, db_session: Session):
    product = models.Product(name="Insufficient Stock Product", price=30.0, stock=10)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = test_client.post(
        "/api/v1/stock/out-return",
        json={"product_id": product.id, "quantity": 20} # Trying to return more than available
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Insufficient stock for return"

    # Verify stock has not changed by re-fetching it
    updated_product = db_session.get(models.Product, product.id)
    assert updated_product.stock == 10

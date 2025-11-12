from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models, schemas

def test_create_product(test_client: TestClient, db_session: Session):
    response = test_client.post(
        "/api/v1/products/",
        json={"name": "Test Product", "description": "A test product", "price": 10.50, "stock_quantity": 100, "category": "Test"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["stock_quantity"] == 100

    # Verify stock movement was created
    movement = db_session.query(models.StockMovement).filter_by(product_id=data["id"]).first()
    assert movement is not None
    assert movement.quantity == 100
    assert movement.movement_type == 'initial'

def test_read_product(test_client: TestClient, db_session: Session):
    product = models.Product(name="Readable Product", price=20.0, stock_quantity=50)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = test_client.get(f"/api/v1/products/{product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Readable Product"
    assert data["id"] == product.id

def test_update_product(test_client: TestClient, db_session: Session):
    product = models.Product(name="Original Name", price=30.0, stock_quantity=30, category="Orig Cat")
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    update_payload = {
        "name": "Updated Name", 
        "price": 35.50, 
        "description": "Updated description", 
        "stock_quantity": 30, # This field is required by ProductCreate schema
        "category": "Updated Cat"
    }

    response = test_client.put(
        f"/api/v1/products/{product.id}",
        json=update_payload
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["price"] == 35.50

def test_delete_product(test_client: TestClient, db_session: Session):
    product = models.Product(name="Deletable Product", price=40.0, stock_quantity=40)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    movement = models.StockMovement(product_id=product.id, quantity=40, movement_type='initial')
    db_session.add(movement)
    db_session.commit()

    response = test_client.delete(f"/api/v1/products/{product.id}")
    assert response.status_code == 204

    deleted_product = db_session.get(models.Product, product.id)
    assert deleted_product is None

    deleted_movement = db_session.query(models.StockMovement).filter_by(product_id=product.id).first()
    assert deleted_movement is None

def test_list_products(test_client: TestClient, db_session: Session):
    db_session.add(models.Product(name="Product A", price=1.0, stock_quantity=1))
    db_session.add(models.Product(name="Product B", price=2.0, stock_quantity=2))
    db_session.commit()

    response = test_client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert "Product A" in [p["name"] for p in data]
    assert "Product B" in [p["name"] for p in data]

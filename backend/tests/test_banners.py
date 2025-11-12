from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models

def test_create_banner(test_client: TestClient):
    response = test_client.post(
        "/api/v1/banners/",
        json={
            "image_url": "/images/test_banner.jpg",
            "link_url": "/products/1",
            "is_active": True,
            "sort_order": 10
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["image_url"] == "/images/test_banner.jpg"
    assert data["is_active"] == True

def test_read_banner(test_client: TestClient, db_session: Session):
    banner = models.Banner(image_url="/images/readable.jpg", link_url="/home", is_active=True, sort_order=1)
    db_session.add(banner)
    db_session.commit()
    db_session.refresh(banner)

    response = test_client.get(f"/api/v1/banners/{banner.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["link_url"] == "/home"

def test_update_banner(test_client: TestClient, db_session: Session):
    banner = models.Banner(image_url="/images/original.jpg", link_url="/orig", is_active=True, sort_order=5)
    db_session.add(banner)
    db_session.commit()
    db_session.refresh(banner)

    response = test_client.put(
        f"/api/v1/banners/{banner.id}",
        json={"image_url": "/images/updated.jpg", "link_url": "/updated", "is_active": False, "sort_order": 1}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["link_url"] == "/updated"
    assert data["is_active"] is False

def test_delete_banner(test_client: TestClient, db_session: Session):
    banner = models.Banner(image_url="/images/deletable.jpg", link_url="/delete", is_active=True, sort_order=1)
    db_session.add(banner)
    db_session.commit()
    db_session.refresh(banner)

    response = test_client.delete(f"/api/v1/banners/{banner.id}")
    assert response.status_code == 204

    # Verify that the banner is deleted by trying to fetch it again
    response = test_client.get(f"/api/v1/banners/{banner.id}")
    assert response.status_code == 404

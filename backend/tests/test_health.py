import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_ping(monkeypatch, client: TestClient):
    def mock_execute(_):
        return None

    def get_db_override():
        class DummySession:
            def execute(self, query):
                return mock_execute(query)

            def close(self):
                pass

        yield DummySession()

    app.dependency_overrides.clear()

    from app.core.database import get_db

    app.dependency_overrides[get_db] = get_db_override

    response = client.get("/health/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

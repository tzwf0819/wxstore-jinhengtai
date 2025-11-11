import io
from fastapi.testclient import TestClient

def test_upload_file(test_client: TestClient):
    # Create a dummy file in memory
    file_content = b"this is a test file content"
    file_like_object = io.BytesIO(file_content)

    response = test_client.post(
        "/api/v1/uploads/",  # Corrected endpoint
        files={"file": ("test_upload.txt", file_like_object, "text/plain")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "file_url" in data
    # The URL should be relative and start with /static/images/
    assert data["file_url"].startswith("/static/images/")
    assert data["file_url"].endswith("test_upload.txt")

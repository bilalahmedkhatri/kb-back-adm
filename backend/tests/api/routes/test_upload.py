import io
from fastapi.testclient import TestClient

from app.core.config import settings


def test_upload_image_success(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    file_content = b"fake image content"
    file = io.BytesIO(file_content)

    response = client.post(
        f"{settings.API_V1_STR}/utils/upload",
        headers=superuser_token_headers,
        files={"file": ("test_avatar.png", file, "image/png")},
    )

    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert data["url"].startswith("/static/uploads/")
    assert data["filename"].endswith(".png")


def test_upload_invalid_extension(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    file_content = b"fake executable content"
    file = io.BytesIO(file_content)

    response = client.post(
        f"{settings.API_V1_STR}/utils/upload",
        headers=superuser_token_headers,
        files={"file": ("test_script.exe", file, "application/octet-stream")},
    )

    assert response.status_code == 400
    assert "Invalid file extension" in response.json()["detail"]

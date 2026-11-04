import uuid
from fastapi.testclient import TestClient
from app.core.config import settings


def test_google_sso_flow(client: TestClient) -> None:
    email = f"google_user_{uuid.uuid4().hex[:6]}@example.com"
    r = client.post(
        f"{settings.API_V1_STR}/auth/google",
        json={
            "credential": f"google_token_{uuid.uuid4().hex}",
            "email": email,
            "full_name": "Google Test User",
            "avatar_url": "https://lh3.googleusercontent.com/a/default-user",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

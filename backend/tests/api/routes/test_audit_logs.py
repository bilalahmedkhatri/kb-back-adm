from fastapi.testclient import TestClient
from app.core.config import settings


def test_audit_logs(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/admin/audit-logs",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert "data" in r.json()
    assert "count" in r.json()

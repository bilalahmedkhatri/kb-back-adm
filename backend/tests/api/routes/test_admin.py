from fastapi.testclient import TestClient

from app.core.config import settings


def test_read_admin_stats(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    normal_user_token_headers: dict[str, str],
) -> None:
    # 1. Normal user forbidden
    res_normal = client.get(
        f"{settings.API_V1_STR}/admin/stats",
        headers=normal_user_token_headers,
    )
    assert res_normal.status_code == 403

    # 2. Superuser/Admin success
    res_admin = client.get(
        f"{settings.API_V1_STR}/admin/stats",
        headers=superuser_token_headers,
    )
    assert res_admin.status_code == 200
    data = res_admin.json()
    assert "total_users" in data
    assert "total_vendors" in data
    assert "pending_vendors" in data
    assert "total_products" in data
    assert "total_orders" in data
    assert "total_revenue" in data

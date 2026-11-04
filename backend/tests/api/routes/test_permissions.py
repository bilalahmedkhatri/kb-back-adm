import uuid
from fastapi.testclient import TestClient
from app.core.config import settings


def test_customer_cannot_access_admin_stats(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/admin/stats",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Admin privileges required"


def test_customer_cannot_access_admin_audit_logs(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/admin/audit-logs",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Admin privileges required"


def test_customer_cannot_create_products(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json={
            "name": "Forbidden Product",
            "description": "Customer attempting to create product",
            "price": 100.0,
            "category": "Jewelry",
            "origin_island": "Tarawa",
            "stock": 10,
        },
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Only vendors or admins can create products"


def test_customer_cannot_verify_vendors(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    fake_profile_id = str(uuid.uuid4())
    r = client.patch(
        f"{settings.API_V1_STR}/vendors/{fake_profile_id}/verify",
        headers=normal_user_token_headers,
        json={"status": "verified"},
    )
    assert r.status_code == 403

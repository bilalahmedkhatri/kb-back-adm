from fastapi.testclient import TestClient
from app.core.config import settings


def test_payments_flow(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    # 1. Create payment intent
    r = client.post(
        f"{settings.API_V1_STR}/payments/intent",
        headers=normal_user_token_headers,
        json={
            "amount": 150.0,
            "currency": "AUD",
            "provider": "stripe",
            "payment_method_details": {"card_brand": "Visa", "last4": "4242"},
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["amount"] == 150.0
    assert data["provider"] == "stripe"
    assert data["status"] == "succeeded"

    # 2. Get my payments
    r_get = client.get(
        f"{settings.API_V1_STR}/payments/me",
        headers=normal_user_token_headers,
    )
    assert r_get.status_code == 200
    assert r_get.json()["count"] >= 1

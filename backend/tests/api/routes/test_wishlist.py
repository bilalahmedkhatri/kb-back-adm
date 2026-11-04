import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.core.config import settings


def test_wishlist_flow(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    target_id = str(uuid.uuid4())
    # 1. Add to wishlist
    r = client.post(
        f"{settings.API_V1_STR}/wishlist/",
        headers=normal_user_token_headers,
        json={"target_id": target_id, "target_type": "product"},
    )
    assert r.status_code == 200
    data = r.json()
    item_id = data["id"]
    assert data["target_id"] == target_id
    assert data["target_type"] == "product"

    # 2. Get my wishlist
    r_get = client.get(
        f"{settings.API_V1_STR}/wishlist/",
        headers=normal_user_token_headers,
    )
    assert r_get.status_code == 200
    assert r_get.json()["count"] >= 1

    # 3. Delete from wishlist
    r_del = client.delete(
        f"{settings.API_V1_STR}/wishlist/{item_id}",
        headers=normal_user_token_headers,
    )
    assert r_del.status_code == 200
    assert r_del.json()["message"] == "Wishlist item removed successfully"

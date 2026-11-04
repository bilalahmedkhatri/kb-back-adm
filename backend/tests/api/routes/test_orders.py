import uuid
from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_order_and_read_my_orders(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    superuser_token_headers: dict[str, str],
) -> None:
    # 1. Create a product first as superuser
    product_data = {
        "name": "Local Dried Coconut Candy",
        "description": "Sweet snack from South Tarawa",
        "price": 12.5,
        "currency": "AUD",
        "category": "Food",
        "origin_island": "Tarawa",
        "material": "Coconut & Sugar",
        "stock": 50,
        "images": [],
    }
    prod_res = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=product_data,
    )
    assert prod_res.status_code == 200
    product_id = prod_res.json()["id"]

    # 2. Create an order as normal user
    order_data = {
        "subtotal": 25.0,
        "delivery_fee": 15.0,
        "tax": 0.0,
        "total": 40.0,
        "currency": "AUD",
        "shipping_address": {
            "full_name": "Test Customer",
            "address": "Bairiki Village",
            "island": "Tarawa",
            "country": "Kiribati",
        },
        "items": [
            {
                "product_id": product_id,
                "name": "Local Dried Coconut Candy",
                "price": 12.5,
                "quantity": 2,
                "image": None,
            }
        ],
    }

    order_res = client.post(
        f"{settings.API_V1_STR}/orders/",
        headers=normal_user_token_headers,
        json=order_data,
    )
    assert order_res.status_code == 200
    order_content = order_res.json()
    assert order_content["total"] == 40.0
    assert len(order_content["items"]) == 1
    assert order_content["status"] == "pending"
    order_id = order_content["id"]

    # 3. Read user's own orders (/orders/me)
    me_res = client.get(
        f"{settings.API_V1_STR}/orders/me",
        headers=normal_user_token_headers,
    )
    assert me_res.status_code == 200
    me_content = me_res.json()
    assert me_content["count"] >= 1
    assert any(o["id"] == order_id for o in me_content["data"])

    # 4. Read specific order by ID (/orders/{id})
    get_res = client.get(
        f"{settings.API_V1_STR}/orders/{order_id}",
        headers=normal_user_token_headers,
    )
    assert get_res.status_code == 200
    assert get_res.json()["id"] == order_id

    # 5. Update order status as admin (/orders/{id}/status)
    status_data = {"status": "confirmed", "tracking_number": "KB-123456"}
    update_res = client.patch(
        f"{settings.API_V1_STR}/orders/{order_id}/status",
        headers=superuser_token_headers,
        json=status_data,
    )
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "confirmed"
    assert update_res.json()["tracking_number"] == "KB-123456"


def test_read_all_orders_admin_only(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    superuser_token_headers: dict[str, str],
) -> None:
    # Normal user should be forbidden
    res_normal = client.get(
        f"{settings.API_V1_STR}/orders/",
        headers=normal_user_token_headers,
    )
    assert res_normal.status_code == 403

    # Superuser/Admin should succeed
    res_admin = client.get(
        f"{settings.API_V1_STR}/orders/",
        headers=superuser_token_headers,
    )
    assert res_admin.status_code == 200
    assert "data" in res_admin.json()
    assert "count" in res_admin.json()

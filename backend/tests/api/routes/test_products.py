import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.modules.products.models import Product
from app.modules.users.models import User, UserRole


def test_read_products(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/products/")
    assert response.status_code == 200
    content = response.json()
    assert "data" in content
    assert "count" in content
    assert isinstance(content["data"], list)


def test_create_product_forbidden_for_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    data = {
        "name": "Handcrafted Pandanus Mat",
        "description": "Traditional Kiribati woven mat",
        "price": 45.0,
        "currency": "AUD",
        "category": "Crafts",
        "origin_island": "Tarawa",
        "material": "Pandanus leaves",
        "stock": 5,
        "images": [],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Only vendors or admins can create products"


def test_create_product_as_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "name": "Kiribati Teiti (Shell Necklace)",
        "description": "Authentic shell necklace made on Abaiang island",
        "price": 25.0,
        "currency": "AUD",
        "category": "Jewelry",
        "origin_island": "Abaiang",
        "material": "Shells & Fibre",
        "stock": 10,
        "images": ["https://example.com/necklace.jpg"],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["price"] == data["price"]
    assert content["category"] == data["category"]
    assert "id" in content


def test_read_product_by_id(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "name": "Unique Carved Wooden Shark Tooth Sword",
        "description": "Decorative artifact inspired by traditional weapons",
        "price": 150.0,
        "currency": "AUD",
        "category": "Artifacts",
        "origin_island": "Tabiteuea",
        "material": "Wood & Resin",
        "stock": 2,
        "images": [],
    }
    create_res = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
    )
    product_id = create_res.json()["id"]

    get_res = client.get(f"{settings.API_V1_STR}/products/{product_id}")
    assert get_res.status_code == 200
    content = get_res.json()
    assert content["id"] == product_id
    assert content["name"] == data["name"]


def test_read_product_not_found(client: TestClient) -> None:
    random_id = uuid.uuid4()
    response = client.get(f"{settings.API_V1_STR}/products/{random_id}")
    assert response.status_code == 404

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.item import create_random_product


def test_read_random_product(client: TestClient, db: Session) -> None:
    product = create_random_product(db)
    response = client.get(f"{settings.API_V1_STR}/products/{product.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == product.name
    assert content["id"] == str(product.id)

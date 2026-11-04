from fastapi.testclient import TestClient

from app.core.config import settings


def test_read_vendor_stats_and_vendor_orders(
    client: TestClient,
    superuser_token_headers: dict[str, str],
) -> None:
    # 1. Vendor stats endpoint
    res_stats = client.get(
        f"{settings.API_V1_STR}/vendors/me/stats",
        headers=superuser_token_headers,
    )
    assert res_stats.status_code == 200
    data_stats = res_stats.json()
    assert "total_products" in data_stats
    assert "active_products" in data_stats
    assert "total_orders" in data_stats
    assert "total_revenue" in data_stats

    # 2. Vendor orders endpoint
    res_orders = client.get(
        f"{settings.API_V1_STR}/orders/vendor",
        headers=superuser_token_headers,
    )
    assert res_orders.status_code == 200
    data_orders = res_orders.json()
    assert "data" in data_orders
    assert "count" in data_orders

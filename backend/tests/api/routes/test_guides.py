from fastapi.testclient import TestClient
from app.core.config import settings


def test_guides_crud_flow(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    # 1. Create guide (Admin)
    r = client.post(
        f"{settings.API_V1_STR}/guides/",
        headers=superuser_token_headers,
        json={
            "title": "Test Kiribati Tourism Guide",
            "excerpt": "A test excerpt for tourism guide",
            "content": "Full detailed content about Kiribati tourism",
            "image": "https://picsum.photos/seed/testguide/800/500",
            "topic": "Travel & Nature",
            "read_time": 5,
            "featured": True,
        },
    )
    assert r.status_code == 200
    data = r.json()
    guide_id = data["id"]
    slug = data["slug"]
    assert data["title"] == "Test Kiribati Tourism Guide"

    # 2. Get list of guides (Public)
    r_list = client.get(f"{settings.API_V1_STR}/guides/")
    assert r_list.status_code == 200
    assert r_list.json()["count"] >= 1

    # 3. Get guide by slug (Public)
    r_get = client.get(f"{settings.API_V1_STR}/guides/{slug}")
    assert r_get.status_code == 200
    assert r_get.json()["id"] == guide_id

    # 4. Delete guide (Admin)
    r_del = client.delete(
        f"{settings.API_V1_STR}/guides/{guide_id}",
        headers=superuser_token_headers,
    )
    assert r_del.status_code == 200
    assert r_del.json()["message"] == "Guide article deleted successfully"

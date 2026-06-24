from pathlib import Path

import pytest
import requests


# Module: live Shopify readiness + storefront catalog/detail integration checks
def _load_frontend_env_url() -> str:
    env_path = Path("/app/frontend/.env")
    if not env_path.exists():
        raise RuntimeError("Missing /app/frontend/.env for REACT_APP_BACKEND_URL")

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "REACT_APP_BACKEND_URL":
            parsed = value.strip().strip('"').strip("'")
            if not parsed:
                raise RuntimeError("REACT_APP_BACKEND_URL is empty in /app/frontend/.env")
            return parsed.rstrip("/")

    raise RuntimeError("REACT_APP_BACKEND_URL not found in /app/frontend/.env")


BASE_URL = _load_frontend_env_url()


@pytest.fixture
def api_client():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


def test_shopify_readiness_connected(api_client):
    response = api_client.get(f"{BASE_URL}/api/shopify/readiness")
    assert response.status_code == 200

    data = response.json()
    assert data["connection_ready"] is True
    assert "connected" in data["next_step"].lower()
    assert "products" in data["supported_sync_targets"]


def test_shop_page_products_present(api_client):
    response = api_client.get(f"{BASE_URL}/api/catalog/products")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["items"], list)
    assert data["total"] > 0
    assert len(data["items"]) > 0

    first_item = data["items"][0]
    assert isinstance(first_item["id"], str) and len(first_item["id"]) > 0
    assert isinstance(first_item["slug"], str) and len(first_item["slug"]) > 0
    assert isinstance(first_item["name"], str) and len(first_item["name"]) > 0


def test_category_filters_rings_and_grills(api_client):
    rings_response = api_client.get(f"{BASE_URL}/api/catalog/products", params={"category": "Rings"})
    grills_response = api_client.get(f"{BASE_URL}/api/catalog/products", params={"category": "Grills"})

    assert rings_response.status_code == 200
    assert grills_response.status_code == 200

    rings_data = rings_response.json()
    grills_data = grills_response.json()

    assert rings_data["total"] > 0
    assert grills_data["total"] > 0
    assert all(item["category"] == "Rings" for item in rings_data["items"])
    assert all(item["category"] == "Grills" for item in grills_data["items"])


def test_product_detail_opens_from_live_listing(api_client):
    listing_response = api_client.get(f"{BASE_URL}/api/catalog/products")
    assert listing_response.status_code == 200
    listing_data = listing_response.json()
    assert listing_data["total"] > 0

    first_product = listing_data["items"][0]
    slug = first_product["slug"]

    detail_response = api_client.get(f"{BASE_URL}/api/catalog/products/{slug}")
    assert detail_response.status_code == 200
    detail_data = detail_response.json()

    assert detail_data["slug"] == slug
    assert detail_data["name"] == first_product["name"]
    assert isinstance(detail_data["gallery"], list) and len(detail_data["gallery"]) > 0
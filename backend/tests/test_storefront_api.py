import json
from pathlib import Path

import pytest
import requests


# Module: storefront API health/catalog/bespoke/shopify-readiness coverage
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


def test_api_root(api_client):
    response = api_client.get(f"{BASE_URL}/api/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Royal Spark API is running."


def test_catalog_home(api_client):
    response = api_client.get(f"{BASE_URL}/api/catalog/home")
    assert response.status_code == 200
    data = response.json()

    assert data["hero_product"] is None
    assert isinstance(data["featured_products"], list) and len(data["featured_products"]) == 0
    assert isinstance(data["collections"], list) and len(data["collections"]) > 0
    assert "atelier_story" in data and isinstance(data["atelier_story"], dict)


def test_catalog_products_default(api_client):
    response = api_client.get(f"{BASE_URL}/api/catalog/products")
    assert response.status_code == 200
    data = response.json()

    assert data["total"] >= 0
    assert isinstance(data["items"], list)
    assert data["categories"][0] == "All"


def test_catalog_products_grills_filter(api_client):
    response = api_client.get(f"{BASE_URL}/api/catalog/products", params={"category": "Grills"})
    assert response.status_code == 200
    data = response.json()

    assert data["total"] >= 0
    assert isinstance(data["items"], list)
    assert all(item["category"] == "Grills" for item in data["items"])


def test_catalog_product_by_specific_slug(api_client):
    listing_response = api_client.get(f"{BASE_URL}/api/catalog/products")
    assert listing_response.status_code == 200
    listing_data = listing_response.json()
    if listing_data["items"]:
        slug = listing_data["items"][0]["slug"]
        response = api_client.get(f"{BASE_URL}/api/catalog/products/{slug}")
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == slug
        assert isinstance(data["gallery"], list) and len(data["gallery"]) >= 1
    else:
        response = api_client.get(f"{BASE_URL}/api/catalog/products/royal-solitaire-spark-ring")
        assert response.status_code == 404


def test_catalog_product_by_slug(api_client):
    response = api_client.get(f"{BASE_URL}/api/catalog/products/shopify-gems-2")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"


def test_bespoke_inquiry_submit(api_client):
    payload = {
        "name": "TEST_Concierge User",
        "email": "test.concierge@example.com",
        "jewelry_type": "Custom Ring",
        "budget": "5,000 - 10,000",
        "material_preference": "Platinum",
        "inspiration": "https://example.com/inspiration",
        "timeline": "Within 1-2 months",
        "message": "TEST Please design a solitaire ring with pavé band.",
    }
    response = api_client.post(
        f"{BASE_URL}/api/bespoke-inquiries",
        data=json.dumps(payload),
    )
    assert response.status_code == 201
    data = response.json()

    assert isinstance(data["id"], str) and len(data["id"]) > 0
    assert data["status"] == "received"
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["jewelry_type"] == payload["jewelry_type"]


def test_shopify_readiness_info(api_client):
    response = api_client.get(f"{BASE_URL}/api/shopify/readiness")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data["connection_ready"], bool)
    assert isinstance(data["next_step"], str) and len(data["next_step"]) > 10
    assert "products" in data["supported_sync_targets"]

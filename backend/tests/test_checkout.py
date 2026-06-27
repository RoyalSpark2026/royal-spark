import os
from pathlib import Path

import pytest
import requests


# Module: Shopify checkout flow + variant_id presence
def _load_frontend_env_url() -> str:
    env_path = Path("/app/frontend/.env")
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "REACT_APP_BACKEND_URL":
            return value.strip().strip('"').strip("'").rstrip("/")
    raise RuntimeError("REACT_APP_BACKEND_URL not found")


BASE_URL = _load_frontend_env_url()


def _shopify_domain() -> str:
    env_path = Path("/app/backend/.env")
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("SHOPIFY_STORE_DOMAIN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


SHOPIFY_DOMAIN = _shopify_domain()


@pytest.fixture
def api_client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# --- variant_id presence in catalog ---
def test_catalog_products_have_variant_id(api_client):
    r = api_client.get(f"{BASE_URL}/api/catalog/products")
    assert r.status_code == 200
    items = r.json()["items"]
    assert len(items) > 0, "Expected live Shopify products"
    missing = [i for i in items if not i.get("variant_id")]
    assert not missing, f"Items missing variant_id: {[m['slug'] for m in missing][:5]}"
    # numeric string
    for it in items[:3]:
        assert it["variant_id"].isdigit(), f"variant_id must be numeric string, got {it['variant_id']}"


def test_catalog_home_featured_have_variant_id(api_client):
    r = api_client.get(f"{BASE_URL}/api/catalog/home")
    assert r.status_code == 200
    featured = r.json()["featured_products"]
    if not featured:
        pytest.skip("No featured products to check")
    for it in featured:
        assert it.get("variant_id"), f"Featured product {it['slug']} missing variant_id"
        assert it["variant_id"].isdigit()


# --- /api/checkout ---
def test_checkout_success_two_items(api_client):
    payload = {"items": [
        {"variant_id": "123", "quantity": 2},
        {"variant_id": "456", "quantity": 1},
    ]}
    r = api_client.post(f"{BASE_URL}/api/checkout", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "checkout_url" in data
    url = data["checkout_url"]
    assert url.startswith("https://")
    assert "/cart/123:2,456:1" in url
    if SHOPIFY_DOMAIN:
        assert SHOPIFY_DOMAIN in url


def test_checkout_success_real_variant(api_client):
    # Use real variant_id from catalog
    products = api_client.get(f"{BASE_URL}/api/catalog/products").json()["items"]
    if not products:
        pytest.skip("No products")
    vid = products[0]["variant_id"]
    r = api_client.post(f"{BASE_URL}/api/checkout", json={
        "items": [{"variant_id": vid, "quantity": 1}]
    })
    assert r.status_code == 200
    assert f"/cart/{vid}:1" in r.json()["checkout_url"]


def test_checkout_empty_items_returns_400(api_client):
    r = api_client.post(f"{BASE_URL}/api/checkout", json={"items": []})
    assert r.status_code == 400


def test_checkout_filters_invalid_variant_ids(api_client):
    # All invalid -> 400
    r = api_client.post(f"{BASE_URL}/api/checkout", json={"items": [
        {"variant_id": "None", "quantity": 1},
        {"variant_id": "null", "quantity": 1},
        {"variant_id": "", "quantity": 1},
    ]})
    assert r.status_code in (400, 422)  # 422 if pydantic rejects empty string


def test_checkout_mixed_valid_and_invalid(api_client):
    r = api_client.post(f"{BASE_URL}/api/checkout", json={"items": [
        {"variant_id": "None", "quantity": 1},
        {"variant_id": "789", "quantity": 3},
    ]})
    assert r.status_code == 200
    url = r.json()["checkout_url"]
    assert "789:3" in url
    assert "None" not in url

"""Verifies the Shopify Admin token auto-refresh fix.

Bug: dev-dashboard app Admin API tokens expire every ~24h, causing 502s
and the homepage to be stuck on 'Curating the collection…'.

Fix: backend now calls fetch_shopify_token_via_client_credentials() against
/admin/oauth/access_token with client_id+client_secret, caches the token,
and refreshes ~5 min before expiry.

These tests hit the live preview backend (no mocking) to confirm the
endpoints actually serve live Shopify data after the fix.
"""

import os
import re

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://spark-mobile-fix.preview.emergentagent.com").rstrip("/")
SHOPIFY_DOMAIN = "royal-spark-jewelry-3.myshopify.com"


@pytest.fixture(scope="module")
def api():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# --- Shopify readiness (must show connection_ready=true with auto token) ---
class TestShopifyReadiness:
    def test_readiness_connected(self, api):
        r = api.get(f"{BASE_URL}/api/shopify/readiness", timeout=30)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data.get("connection_ready") is True
        assert data.get("has_store_domain") is True
        assert data.get("has_admin_token") is True


# --- Catalog: live products with numeric variant_id ---
class TestCatalogProducts:
    def test_products_returns_42_with_numeric_variant_ids(self, api):
        r = api.get(f"{BASE_URL}/api/catalog/products", timeout=60)
        assert r.status_code == 200, r.text
        data = r.json()
        # Expected live count per problem statement
        assert data.get("total") == 42, f"Expected total=42, got {data.get('total')}"
        items = data.get("items") or []
        assert len(items) == 42
        # Every item must have a numeric variant_id (string of digits)
        for it in items:
            vid = it.get("variant_id")
            assert vid is not None and str(vid).isdigit(), f"Bad variant_id on {it.get('slug')}: {vid!r}"

    def test_home_featured_products_populated(self, api):
        r = api.get(f"{BASE_URL}/api/catalog/home", timeout=60)
        assert r.status_code == 200, r.text
        data = r.json()
        featured = data.get("featured_products") or []
        assert len(featured) > 0, "featured_products should be non-empty"
        # Each featured should have a numeric variant_id too
        for p in featured:
            assert str(p.get("variant_id", "")).isdigit()

    def test_product_detail_by_real_slug(self, api):
        # Fetch a real slug from the catalog (request mentions 'spark-mobile-fix'
        # which is the preview subdomain, not a slug). Use first live product instead.
        listing = api.get(f"{BASE_URL}/api/catalog/products", timeout=60).json()
        slug = listing["items"][0]["slug"]
        r = api.get(f"{BASE_URL}/api/catalog/products/{slug}", timeout=30)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data.get("slug") == slug
        assert str(data.get("variant_id", "")).isdigit()


# --- Checkout still works on top of the refreshed token plumbing ---
class TestCheckout:
    def test_checkout_returns_cart_permalink(self, api):
        payload = {"items": [{"variant_id": "123", "quantity": 1}]}
        r = api.post(f"{BASE_URL}/api/checkout", json=payload, timeout=30)
        assert r.status_code == 200, r.text
        url = r.json().get("checkout_url", "")
        assert url == f"https://{SHOPIFY_DOMAIN}/cart/123:1"

    def test_checkout_empty_items_rejected(self, api):
        r = api.post(f"{BASE_URL}/api/checkout", json={"items": []}, timeout=30)
        assert r.status_code == 400

    def test_checkout_with_live_variant_id(self, api):
        # End-to-end-ish: pull a live variant_id then build the permalink
        listing = api.get(f"{BASE_URL}/api/catalog/products", timeout=60).json()
        live_vid = listing["items"][0]["variant_id"]
        r = api.post(
            f"{BASE_URL}/api/checkout",
            json={"items": [{"variant_id": live_vid, "quantity": 2}]},
            timeout=30,
        )
        assert r.status_code == 200, r.text
        url = r.json()["checkout_url"]
        assert url == f"https://{SHOPIFY_DOMAIN}/cart/{live_vid}:2"
        # Sanity: URL shape
        assert re.match(rf"^https://{re.escape(SHOPIFY_DOMAIN)}/cart/\d+:\d+$", url)

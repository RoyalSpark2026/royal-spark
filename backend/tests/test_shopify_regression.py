"""Regression tests: base64-encoded Shopify client secret should not break token/catalog."""
import os
import requests
import pytest

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://spark-mobile-fix.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"


def test_catalog_home_returns_6_featured_with_hero_images():
    r = requests.get(f"{API}/catalog/home", timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    featured = data.get("featured_products") or data.get("featured") or []
    assert len(featured) == 6, f"Expected 6 featured, got {len(featured)}: keys={list(data.keys())}"
    for p in featured:
        hero = p.get("hero_image") or p.get("image")
        assert hero and isinstance(hero, str) and hero.startswith("http"), f"Bad hero_image: {hero} in {p.get('title')}"


def test_catalog_products_returns_all_with_variant_id():
    r = requests.get(f"{API}/catalog/products", timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    products = data.get("items") or data.get("products") if isinstance(data, dict) else data
    assert isinstance(products, list)
    assert len(products) >= 40, f"Expected ~53 products, got {len(products)}"
    for p in products[:10]:
        vid = p.get("variant_id") or (p.get("variants", [{}])[0].get("id") if p.get("variants") else None)
        assert vid is not None, f"Missing variant_id for {p.get('title')}"
        # numeric check
        assert str(vid).isdigit(), f"variant_id not numeric: {vid}"


def test_shopify_readiness():
    r = requests.get(f"{API}/shopify/readiness", timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("connection_ready") is True, f"connection_ready not true: {data}"


def test_checkout_returns_shopify_permalink():
    # First get a real variant_id from products
    prods = requests.get(f"{API}/catalog/products", timeout=30).json()
    products = prods.get("items") or prods.get("products") if isinstance(prods, dict) else prods
    variant_id = None
    for p in products:
        vid = p.get("variant_id") or (p.get("variants", [{}])[0].get("id") if p.get("variants") else None)
        if vid:
            variant_id = str(vid)
            break
    assert variant_id, "Could not find any variant_id"

    r = requests.post(f"{API}/checkout", json={"items": [{"variant_id": variant_id, "quantity": 1}]}, timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    url = data.get("checkout_url") or data.get("url")
    assert url and "http" in url, f"No checkout_url: {data}"
    # Shopify cart permalink typically contains /cart/
    assert "cart" in url.lower() or "checkout" in url.lower(), f"Not a Shopify checkout url: {url}"


def test_cors_allows_royalsparkjewelry_origin():
    origin = "https://www.royalsparkjewelry.com"
    r = requests.get(f"{API}/catalog/home", headers={"Origin": origin}, timeout=30)
    assert r.status_code == 200
    acao = r.headers.get("access-control-allow-origin") or r.headers.get("Access-Control-Allow-Origin")
    assert acao is not None, f"Missing CORS header. Headers: {dict(r.headers)}"
    assert acao == origin or acao == "*", f"Unexpected ACAO: {acao}"

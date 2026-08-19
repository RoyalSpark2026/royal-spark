#!/usr/bin/env python3
"""Focused API/static asset verification for Royal Spark iteration 16."""

import json
import importlib.util
import os
from pathlib import Path

import requests


BASE_URL = "https://spark-mobile-fix.preview.emergentagent.com"
ORIGIN = "https://www.royalsparkjewelry.com"
OUT = Path("/app/test_reports/royal_spark_iteration16_api_results.json")


def check(condition, message, details=None):
    result = {"pass": bool(condition), "message": message}
    if details is not None:
        result["details"] = details
    print(("PASS" if condition else "FAIL") + f": {message}")
    if details is not None:
        print(json.dumps(details, indent=2)[:1200])
    return result


def main():
    results = []
    session = requests.Session()

    static_paths = [
        "/hero-film.mp4",
        "/hero-film.webm",
        "/hero-poster.jpg",
        "/memories-feature.webm",
        "/customart-feature.webm",
        "/ring-feature.webm",
    ]
    for path in static_paths:
        resp = session.get(BASE_URL + path, timeout=30, stream=True)
        content_type = resp.headers.get("content-type", "")
        content_length = resp.headers.get("content-length")
        results.append(check(resp.status_code == 200, f"static asset {path} returns HTTP 200", {"status": resp.status_code, "content_type": content_type, "content_length": content_length}))
        resp.close()

    home_resp = session.get(BASE_URL + "/api/catalog/home", headers={"Origin": ORIGIN}, timeout=60)
    home_json = home_resp.json() if home_resp.ok else {}
    featured = home_json.get("featured_products") or []
    real_photo_products = [
        p for p in featured
        if p.get("hero_image")
        and not p["hero_image"].split("?")[0].lower().endswith(".svg")
        and not p["hero_image"].endswith("/product-placeholder.png")
    ]
    results.append(check(home_resp.status_code == 200, "GET /api/catalog/home returns 200", {"status": home_resp.status_code}))
    results.append(check(len(featured) == 6 and len(real_photo_products) == 6, "home has 6 featured products with real photo hero_image values", {"featured_count": len(featured), "real_photo_count": len(real_photo_products), "sample_images": [p.get("hero_image") for p in featured[:3]]}))
    aca_origin = home_resp.headers.get("access-control-allow-origin")
    results.append(check(bool(aca_origin), "cross-origin GET includes access-control-allow-origin", {"access_control_allow_origin": aca_origin}))

    products_resp = session.get(BASE_URL + "/api/catalog/products", timeout=60)
    products_json = products_resp.json() if products_resp.ok else {}
    items = products_json.get("items") or []
    numeric_variant_items = [p for p in items if str(p.get("variant_id") or "").isdigit()]
    results.append(check(products_resp.status_code == 200, "GET /api/catalog/products returns 200", {"status": products_resp.status_code, "total": products_json.get("total")}))
    results.append(check(len(items) > 0 and len(numeric_variant_items) == len(items), "all returned products have numeric variant_id", {"item_count": len(items), "numeric_variant_count": len(numeric_variant_items), "sample_variant_id": numeric_variant_items[0].get("variant_id") if numeric_variant_items else None}))

    readiness_resp = session.get(BASE_URL + "/api/shopify/readiness", timeout=30)
    readiness_json = readiness_resp.json() if readiness_resp.ok else {}
    results.append(check(readiness_resp.status_code == 200 and readiness_json.get("connection_ready") is True, "/api/shopify/readiness connection_ready true", {"status": readiness_resp.status_code, "body": readiness_json}))

    checkout_variant = numeric_variant_items[0]["variant_id"] if numeric_variant_items else ""
    checkout_resp = session.post(BASE_URL + "/api/checkout", json={"items": [{"variant_id": checkout_variant, "quantity": 1}]}, timeout=30)
    checkout_json = checkout_resp.json() if checkout_resp.ok else {}
    checkout_url = checkout_json.get("checkout_url", "")
    results.append(check(checkout_resp.status_code == 200 and checkout_url.startswith("https://royal-spark-jewelry-3.myshopify.com/cart/") and str(checkout_variant) in checkout_url, "POST /api/checkout returns Shopify cart permalink", {"status": checkout_resp.status_code, "checkout_url": checkout_url}))

    # Simulate the Railway/client-owned deployment constraint: no SHOPIFY_* or
    # CORS_ORIGINS env vars available. Disable backend/.env loading for this
    # subprocess import so only code defaults can satisfy the catalog request.
    old_env = os.environ.copy()
    try:
        os.environ["MONGO_URL"] = old_env.get("MONGO_URL", "mongodb://localhost:27017")
        os.environ["DB_NAME"] = old_env.get("DB_NAME", "test_database")
        for key in ["SHOPIFY_STORE_DOMAIN", "SHOPIFY_ADMIN_TOKEN", "SHOPIFY_CLIENT_ID", "SHOPIFY_CLIENT_SECRET", "CORS_ORIGINS"]:
            os.environ.pop(key, None)
        import dotenv
        dotenv.load_dotenv = lambda *args, **kwargs: False
        spec = importlib.util.spec_from_file_location("royal_spark_blank_env_server", "/app/backend/server.py")
        server = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(server)
        from fastapi.testclient import TestClient
        blank_client = TestClient(server.app)
        blank_home_resp = blank_client.get("/api/catalog/home", headers={"Origin": ORIGIN}, timeout=90)
        blank_home_json = blank_home_resp.json() if blank_home_resp.status_code == 200 else {}
        blank_featured = blank_home_json.get("featured_products") or []
        results.append(check(
            server.get_shopify_admin_token() is None
            and server.shopify_is_configured() is True
            and blank_home_resp.status_code == 200
            and len(blank_featured) == 6
            and bool(blank_home_resp.headers.get("access-control-allow-origin")),
            "blank SHOPIFY_*/CORS env simulation still returns live home catalog via code defaults",
            {
                "status": blank_home_resp.status_code,
                "featured_count": len(blank_featured),
                "has_admin_token": bool(server.get_shopify_admin_token()),
                "store_domain": server.get_shopify_store_domain(),
                "access_control_allow_origin": blank_home_resp.headers.get("access-control-allow-origin"),
            },
        ))
    finally:
        os.environ.clear()
        os.environ.update(old_env)

    passed = sum(1 for r in results if r["pass"])
    payload = {"base_url": BASE_URL, "passed": passed, "total": len(results), "results": results}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    if passed != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
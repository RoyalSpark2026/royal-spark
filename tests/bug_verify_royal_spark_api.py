"""Focused bug verification for Royal Spark custom-domain catalog/images/CORS fix.

This script intentionally verifies both the deployed preview URL and the local
backend code path with Shopify/CORS env vars blanked, because the production fix
must work from GitHub code only without Railway dashboard env changes.
"""

import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests
from fastapi.testclient import TestClient


PREVIEW_BASE = os.environ.get("PREVIEW_BASE", "https://spark-mobile-fix.preview.emergentagent.com")
ORIGIN = "https://www.royalsparkjewelry.com"
REPORT_PATH = Path("/app/test_reports/royal_spark_api_results.json")


def check(condition: bool, message: str, failures: List[str]) -> None:
    if not condition:
        failures.append(message)


def acao_is_valid(value: str | None) -> bool:
    return value in {"*", ORIGIN}


def image_is_real_photo(url: str, failures: List[str]) -> Dict[str, Any]:
    result: Dict[str, Any] = {"url": url, "status": None, "content_type": None, "bytes": 0}
    check(bool(url), "Product image URL is missing", failures)
    check(not url.lower().split("?")[0].endswith(".svg"), f"Product image is SVG placeholder/icon: {url}", failures)
    check("product-placeholder.png" not in url, f"Featured product uses placeholder image: {url}", failures)
    if not url.startswith("http"):
        url = f"{PREVIEW_BASE}{url}"
    try:
        response = requests.get(url, timeout=30)
        result.update(
            {
                "status": response.status_code,
                "content_type": response.headers.get("content-type", ""),
                "bytes": len(response.content),
            }
        )
        check(response.status_code == 200, f"Image did not return 200: {url} -> {response.status_code}", failures)
        check("image/" in result["content_type"], f"Image response is not image/*: {url} -> {result['content_type']}", failures)
        check("svg" not in result["content_type"].lower(), f"Image response is SVG: {url}", failures)
        check(result["bytes"] > 1000, f"Image response too small to be a real photo: {url} ({result['bytes']} bytes)", failures)
    except Exception as exc:  # noqa: BLE001
        failures.append(f"Image request failed for {url}: {exc}")
    return result


def verify_external_preview() -> Dict[str, Any]:
    failures: List[str] = []
    results: Dict[str, Any] = {"base": PREVIEW_BASE, "origin": ORIGIN, "failures": failures}

    session = requests.Session()

    options = session.options(
        f"{PREVIEW_BASE}/api/catalog/home",
        headers={
            "Origin": ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type",
        },
        timeout=30,
    )
    results["options_catalog_home"] = {
        "status": options.status_code,
        "acao": options.headers.get("access-control-allow-origin"),
        "allow_methods": options.headers.get("access-control-allow-methods"),
    }
    check(options.status_code in {200, 204}, f"OPTIONS /api/catalog/home returned {options.status_code}", failures)
    check(acao_is_valid(options.headers.get("access-control-allow-origin")), f"OPTIONS missing/invalid ACAO: {options.headers.get('access-control-allow-origin')}", failures)
    check(bool(options.headers.get("access-control-allow-methods")), "OPTIONS missing access-control-allow-methods", failures)

    home = session.get(f"{PREVIEW_BASE}/api/catalog/home", headers={"Origin": ORIGIN}, timeout=60)
    results["get_catalog_home"] = {
        "status": home.status_code,
        "acao": home.headers.get("access-control-allow-origin"),
    }
    check(home.status_code == 200, f"GET /api/catalog/home returned {home.status_code}: {home.text[:200]}", failures)
    check(home.headers.get("access-control-allow-origin") == "*", f"Preview GET /api/catalog/home ACAO should be '*', got {home.headers.get('access-control-allow-origin')}", failures)
    home_json = home.json() if home.status_code == 200 else {}
    featured = home_json.get("featured_products") or []
    results["featured_count"] = len(featured)
    results["featured_products"] = [
        {"slug": item.get("slug"), "hero_image": item.get("hero_image"), "variant_id": item.get("variant_id")}
        for item in featured
    ]
    check(len(featured) == 6, f"Expected 6 featured products, got {len(featured)}", failures)
    results["featured_image_checks"] = [image_is_real_photo(item.get("hero_image") or "", failures) for item in featured[:6]]

    products = session.get(f"{PREVIEW_BASE}/api/catalog/products", headers={"Origin": ORIGIN}, timeout=60)
    results["get_catalog_products"] = {
        "status": products.status_code,
        "acao": products.headers.get("access-control-allow-origin"),
    }
    check(products.status_code == 200, f"GET /api/catalog/products returned {products.status_code}: {products.text[:200]}", failures)
    products_json = products.json() if products.status_code == 200 else {}
    items = products_json.get("items") or []
    results["products_total"] = products_json.get("total")
    results["products_returned"] = len(items)
    numeric_variant_count = sum(1 for item in items if str(item.get("variant_id") or "").isdigit())
    results["numeric_variant_count"] = numeric_variant_count
    check(len(items) > 0, "Catalog products returned no items", failures)
    check(numeric_variant_count == len(items), f"Expected every returned product to have numeric variant_id; got {numeric_variant_count}/{len(items)}", failures)

    readiness = session.get(f"{PREVIEW_BASE}/api/shopify/readiness", headers={"Origin": ORIGIN}, timeout=30)
    results["get_shopify_readiness"] = {"status": readiness.status_code, "body": readiness.json() if readiness.status_code == 200 else readiness.text[:200]}
    check(readiness.status_code == 200, f"GET /api/shopify/readiness returned {readiness.status_code}", failures)
    if readiness.status_code == 200:
        check(readiness.json().get("connection_ready") is True, f"Shopify readiness connection_ready is not true: {readiness.json()}", failures)

    if items:
        variant = str(items[0].get("variant_id") or "")
        checkout = session.post(
            f"{PREVIEW_BASE}/api/checkout",
            json={"items": [{"variant_id": variant, "quantity": 1}]},
            headers={"Origin": ORIGIN},
            timeout=30,
        )
        results["post_checkout"] = {"status": checkout.status_code, "body": checkout.json() if checkout.status_code == 200 else checkout.text[:200]}
        check(checkout.status_code == 200, f"POST /api/checkout returned {checkout.status_code}: {checkout.text[:200]}", failures)
        if checkout.status_code == 200:
            checkout_url = checkout.json().get("checkout_url", "")
            check(checkout_url.startswith("https://royal-spark-jewelry-3.myshopify.com/cart/"), f"Checkout URL is not Shopify cart permalink: {checkout_url}", failures)
            check(f"/{variant}:1" in checkout_url, f"Checkout URL does not contain variant quantity path: {checkout_url}", failures)

    placeholder = session.get(f"{PREVIEW_BASE}/product-placeholder.png", timeout=30)
    results["product_placeholder"] = {"status": placeholder.status_code, "content_type": placeholder.headers.get("content-type"), "bytes": len(placeholder.content)}
    check(placeholder.status_code == 200, f"/product-placeholder.png returned {placeholder.status_code}", failures)
    check("image/png" in (placeholder.headers.get("content-type") or ""), f"/product-placeholder.png is not image/png: {placeholder.headers.get('content-type')}", failures)

    return results


def verify_local_blank_env_code_path() -> Dict[str, Any]:
    failures: List[str] = []
    results: Dict[str, Any] = {"failures": failures}

    os.environ["MONGO_URL"] = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    os.environ["DB_NAME"] = os.environ.get("DB_NAME", "test_database")
    for key in ["CORS_ORIGINS", "SHOPIFY_STORE_DOMAIN", "SHOPIFY_CLIENT_ID", "SHOPIFY_CLIENT_SECRET", "SHOPIFY_ADMIN_TOKEN"]:
        os.environ[key] = ""

    sys.path.insert(0, "/app/backend")
    server = importlib.import_module("server")

    results["fallback_getters"] = {
        "store_domain": server.get_shopify_store_domain(),
        "has_client_id": bool(server.get_shopify_client_id()),
        "has_client_secret": bool(server.get_shopify_client_secret()),
        "admin_token": server.get_shopify_admin_token(),
        "shopify_is_configured": server.shopify_is_configured(),
        "allow_all_origins": getattr(server, "allow_all_origins", None),
        "allowed_origins": getattr(server, "allowed_origins", None),
    }
    check(results["fallback_getters"]["store_domain"] == "royal-spark-jewelry-3.myshopify.com", "Blank SHOPIFY_STORE_DOMAIN did not use default fallback", failures)
    check(results["fallback_getters"]["has_client_id"], "Blank SHOPIFY_CLIENT_ID did not use default fallback", failures)
    check(results["fallback_getters"]["has_client_secret"], "Blank SHOPIFY_CLIENT_SECRET did not use default fallback", failures)
    check(results["fallback_getters"]["admin_token"] is None, "SHOPIFY_ADMIN_TOKEN should be None when blank to prove client-credentials path is used", failures)
    check(results["fallback_getters"]["shopify_is_configured"] is True, "Shopify should be configured from fallback client credentials", failures)
    check(results["fallback_getters"]["allowed_origins"] == ["*"], f"Blank CORS_ORIGINS should allow wildcard, got {results['fallback_getters']['allowed_origins']}", failures)

    client = TestClient(server.app)
    preflight = client.options(
        "/api/catalog/home",
        headers={"Origin": ORIGIN, "Access-Control-Request-Method": "GET"},
    )
    results["local_options_catalog_home"] = {
        "status": preflight.status_code,
        "acao": preflight.headers.get("access-control-allow-origin"),
        "allow_methods": preflight.headers.get("access-control-allow-methods"),
    }
    check(preflight.status_code in {200, 204}, f"Local blank-env OPTIONS returned {preflight.status_code}", failures)
    check(preflight.headers.get("access-control-allow-origin") == "*", f"Local blank-env OPTIONS ACAO should be *, got {preflight.headers.get('access-control-allow-origin')}", failures)

    home = client.get("/api/catalog/home", headers={"Origin": ORIGIN})
    results["local_get_catalog_home"] = {"status": home.status_code, "acao": home.headers.get("access-control-allow-origin")}
    check(home.status_code == 200, f"Local blank-env GET /api/catalog/home returned {home.status_code}: {home.text[:200]}", failures)
    check(home.headers.get("access-control-allow-origin") == "*", f"Local blank-env GET ACAO should be *, got {home.headers.get('access-control-allow-origin')}", failures)
    if home.status_code == 200:
        featured = home.json().get("featured_products") or []
        results["local_featured_count"] = len(featured)
        check(len(featured) == 6, f"Local blank-env expected 6 featured products, got {len(featured)}", failures)

    readiness = client.get("/api/shopify/readiness")
    results["local_readiness"] = {"status": readiness.status_code, "body": readiness.json() if readiness.status_code == 200 else readiness.text[:200]}
    check(readiness.status_code == 200, f"Local readiness returned {readiness.status_code}", failures)
    if readiness.status_code == 200:
        check(readiness.json().get("connection_ready") is True, f"Local readiness connection_ready not true: {readiness.json()}", failures)
        check(readiness.json().get("has_admin_token") is False, f"Local blank-env readiness should not depend on static admin token: {readiness.json()}", failures)

    return results


def main() -> int:
    combined = {
        "external_preview": verify_external_preview(),
        "local_blank_env_code_path": verify_local_blank_env_code_path(),
    }
    all_failures = combined["external_preview"]["failures"] + combined["local_blank_env_code_path"]["failures"]
    combined["passed"] = not all_failures
    combined["all_failures"] = all_failures
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(combined, indent=2), encoding="utf-8")
    print(json.dumps(combined, indent=2))
    return 0 if not all_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
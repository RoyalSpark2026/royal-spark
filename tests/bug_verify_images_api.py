#!/usr/bin/env python3
"""Focused API checks for the Royal Spark product-image regression."""

import json
from urllib.parse import urljoin, urlparse

import requests


BASE_URL = "https://spark-mobile-fix.preview.emergentagent.com"
API_URL = f"{BASE_URL}/api"
PLACEHOLDER = "/product-placeholder.png"
MARKETING_BANNER_HINTS = [
    "8jfge9he_fashion-%26-beauty-design-2x",
    "fashion-%26-beauty-design-2x%20%281%29%20%281%29",
    "Royal Sparks Spring/Summer",
]
REAL_PHOTO_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def absolute_url(src: str) -> str:
    return urljoin(BASE_URL, src) if src.startswith("/") else src


def clean_path(src: str) -> str:
    return urlparse(src).path.lower()


def is_real_photo_url(src: str) -> bool:
    path = clean_path(src)
    return path.endswith(REAL_PHOTO_EXTENSIONS) and not path.endswith(".svg") and src != PLACEHOLDER


def fetch_json(path: str):
    response = requests.get(f"{API_URL}{path}", timeout=60)
    response.raise_for_status()
    return response.json()


def check_image_loads(src: str):
    url = absolute_url(src)
    response = requests.get(url, timeout=60, stream=True)
    # Read a small chunk to ensure the body is actually present.
    first_chunk = next(response.iter_content(chunk_size=1024), b"")
    return {
        "url": url,
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type", ""),
        "has_body": bool(first_chunk),
    }


def main():
    failures = []
    evidence = {}

    home = fetch_json("/catalog/home")
    featured = home.get("featured_products", [])
    evidence["featured_count"] = len(featured)
    evidence["featured_images"] = []
    if len(featured) != 6:
        failures.append(f"Expected 6 featured products, got {len(featured)}")

    for product in featured:
        src = product.get("hero_image") or ""
        image_result = check_image_loads(src)
        evidence["featured_images"].append(
            {
                "slug": product.get("slug"),
                "name": product.get("name"),
                "hero_image": src,
                "image_result": image_result,
            }
        )
        if not is_real_photo_url(src):
            failures.append(f"Featured product {product.get('slug')} hero_image is not a real photo URL: {src}")
        if any(hint in src for hint in MARKETING_BANNER_HINTS):
            failures.append(f"Featured product {product.get('slug')} uses marketing banner image: {src}")
        if image_result["status_code"] != 200 or not image_result["content_type"].startswith("image/") or not image_result["has_body"]:
            failures.append(f"Featured product {product.get('slug')} image did not load as an image: {image_result}")

    products_payload = fetch_json("/catalog/products")
    products = products_payload.get("items", [])
    evidence["products_total"] = products_payload.get("total")
    evidence["product_count"] = len(products)
    if products_payload.get("total") != 42 or len(products) != 42:
        failures.append(f"Expected /catalog/products to return 42 products, got total={products_payload.get('total')} count={len(products)}")

    non_numeric_variants = [p.get("slug") for p in products if not str(p.get("variant_id") or "").isdigit()]
    evidence["non_numeric_variant_slugs"] = non_numeric_variants
    if non_numeric_variants:
        failures.append(f"Products with non-numeric variant_id: {non_numeric_variants[:10]}")

    placeholder_result = check_image_loads(PLACEHOLDER)
    evidence["placeholder_result"] = placeholder_result
    if placeholder_result["status_code"] != 200 or not placeholder_result["content_type"].startswith("image/png"):
        failures.append(f"Placeholder image does not return HTTP 200 image/png: {placeholder_result}")

    placeholder_products = [p for p in products if p.get("hero_image") == PLACEHOLDER]
    evidence["placeholder_product_slugs"] = [p.get("slug") for p in placeholder_products]
    # If any product genuinely has no image, verify detail gallery resolves to the branded placeholder.
    if placeholder_products:
        detail = fetch_json(f"/catalog/products/{placeholder_products[0]['slug']}")
        evidence["placeholder_detail"] = {
            "slug": detail.get("slug"),
            "hero_image": detail.get("hero_image"),
            "gallery": detail.get("gallery"),
        }
        if detail.get("hero_image") != PLACEHOLDER or detail.get("gallery") != [PLACEHOLDER]:
            failures.append(f"No-photo product detail did not use placeholder gallery: {evidence['placeholder_detail']}")

    checkout_item = next((p for p in products if str(p.get("variant_id") or "").isdigit()), None)
    if checkout_item:
        checkout_response = requests.post(
            f"{API_URL}/checkout",
            json={"items": [{"variant_id": checkout_item["variant_id"], "quantity": 1}]},
            timeout=60,
        )
        evidence["checkout_status"] = checkout_response.status_code
        evidence["checkout_body"] = checkout_response.json() if checkout_response.headers.get("content-type", "").startswith("application/json") else checkout_response.text[:200]
        if checkout_response.status_code != 200 or "checkout_url" not in evidence["checkout_body"]:
            failures.append(f"Checkout did not return checkout_url: {checkout_response.status_code} {evidence['checkout_body']}")
        elif "/cart/" not in evidence["checkout_body"].get("checkout_url", ""):
            failures.append(f"Checkout URL is not a Shopify cart permalink: {evidence['checkout_body']}")
    else:
        failures.append("No product with numeric variant_id available for checkout regression test")

    result = {"passed": not failures, "failures": failures, "evidence": evidence}
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
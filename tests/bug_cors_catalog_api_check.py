#!/usr/bin/env python3
"""Focused verification for Royal Spark CORS/catalog production symptom.

Checks preview backend and the live Railway backend with the custom-domain Origin
that previously triggered missing Access-Control-Allow-Origin and an endless
"Curating the collection…" frontend state.
"""

import json
import re
from typing import Any, Dict, List

import requests


ORIGIN = "https://www.royalsparkjewelry.com"
BASES = {
    "preview": "https://spark-mobile-fix.preview.emergentagent.com/api",
    "production_railway": "https://royal-spark-production.up.railway.app/api",
}


def record(results: List[Dict[str, Any]], name: str, ok: bool, detail: str, extra: Dict[str, Any] | None = None) -> None:
    results.append({"name": name, "ok": ok, "detail": detail, **(extra or {})})
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")


def get_json(url: str, **kwargs: Any) -> requests.Response:
    return requests.get(url, timeout=45, **kwargs)


def main() -> int:
    results: List[Dict[str, Any]] = []

    for label, base in BASES.items():
        home_url = f"{base}/catalog/home"
        try:
            response = get_json(home_url, headers={"Origin": ORIGIN})
            acao = response.headers.get("access-control-allow-origin")
            ok = response.status_code == 200 and bool(acao) and (acao == "*" or acao == ORIGIN)
            record(
                results,
                f"{label} cross-origin GET /catalog/home CORS",
                ok,
                f"status={response.status_code}, acao={acao!r}",
                {"headers": {"access-control-allow-origin": acao}},
            )
            if response.status_code == 200:
                home = response.json()
                featured = home.get("featured_products") or []
                image_urls = [p.get("hero_image") for p in featured]
                real_images = [u for u in image_urls if u and not u.split("?")[0].lower().endswith(".svg")]
                record(
                    results,
                    f"{label} /catalog/home featured product images",
                    len(featured) == 6 and len(real_images) == 6,
                    f"featured_count={len(featured)}, real_photo_count={len(real_images)}",
                    {"sample_images": real_images[:3]},
                )
            else:
                record(results, f"{label} /catalog/home featured product images", False, "home endpoint not 200")
        except Exception as exc:  # noqa: BLE001
            record(results, f"{label} cross-origin GET /catalog/home CORS", False, repr(exc))

        try:
            preflight = requests.options(
                home_url,
                headers={"Origin": ORIGIN, "Access-Control-Request-Method": "GET"},
                timeout=45,
            )
            acao = preflight.headers.get("access-control-allow-origin")
            methods = preflight.headers.get("access-control-allow-methods")
            ok = preflight.status_code in {200, 204} and bool(acao) and bool(methods) and "GET" in methods.upper()
            record(
                results,
                f"{label} OPTIONS /catalog/home preflight CORS",
                ok,
                f"status={preflight.status_code}, acao={acao!r}, methods={methods!r}",
                {"headers": {"access-control-allow-origin": acao, "access-control-allow-methods": methods}},
            )
        except Exception as exc:  # noqa: BLE001
            record(results, f"{label} OPTIONS /catalog/home preflight CORS", False, repr(exc))

        try:
            products_response = get_json(f"{base}/catalog/products")
            products = products_response.json().get("items") if products_response.status_code == 200 else []
            variant_ids = [str(item.get("variant_id")) for item in products or []]
            numeric_variant_ids = [vid for vid in variant_ids if re.fullmatch(r"\d+", vid or "")]
            record(
                results,
                f"{label} /catalog/products product count and numeric variant_ids",
                products_response.status_code == 200 and len(products or []) >= 1 and len(numeric_variant_ids) == len(products or []),
                f"status={products_response.status_code}, count={len(products or [])}, numeric_variant_ids={len(numeric_variant_ids)}",
            )

            if products:
                first = products[0]
                checkout = requests.post(
                    f"{base}/checkout",
                    json={"items": [{"variant_id": first.get("variant_id"), "quantity": 1}]},
                    timeout=45,
                )
                checkout_url = checkout.json().get("checkout_url") if checkout.status_code == 200 else ""
                record(
                    results,
                    f"{label} POST /checkout returns Shopify cart permalink",
                    checkout.status_code == 200 and checkout_url.startswith("https://") and "/cart/" in checkout_url,
                    f"status={checkout.status_code}, checkout_url={checkout_url}",
                )
            else:
                record(results, f"{label} POST /checkout returns Shopify cart permalink", False, "no product variant available")
        except Exception as exc:  # noqa: BLE001
            record(results, f"{label} /catalog/products and checkout", False, repr(exc))

        try:
            readiness = get_json(f"{base}/shopify/readiness")
            payload = readiness.json() if readiness.status_code == 200 else {}
            record(
                results,
                f"{label} /shopify/readiness connection_ready",
                readiness.status_code == 200 and payload.get("connection_ready") is True,
                f"status={readiness.status_code}, connection_ready={payload.get('connection_ready')}",
            )
        except Exception as exc:  # noqa: BLE001
            record(results, f"{label} /shopify/readiness connection_ready", False, repr(exc))

    print("RESULT_JSON=" + json.dumps(results, indent=2))
    return 0 if all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
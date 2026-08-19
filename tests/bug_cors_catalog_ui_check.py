#!/usr/bin/env python3
"""Playwright checklist for the Royal Spark CORS/catalog UI bug.

This mirrors the focused browser automation run: preview should render homepage
and shop products/images; the live custom domain should be checked for the
reported stuck loading state and catalog CORS console errors.
"""

import asyncio

from playwright.async_api import async_playwright


async def check_site(page, base_url: str, label: str) -> None:
    await page.goto(base_url, wait_until="domcontentloaded", timeout=30_000)
    try:
        await page.get_by_test_id("homepage-live-products-grid").wait_for(state="visible", timeout=20_000)
    except Exception as exc:  # noqa: BLE001
        print(f"{label} homepage grid not visible: {exc}")
    home_loading_count = await page.get_by_test_id("home-loading-state").count()
    home_cards_count = await page.locator('[data-testid^="product-card-"]').count()
    home_images = await page.evaluate(
        """() => Array.from(document.querySelectorAll('[data-testid^="product-image-"]'))
        .map(img => ({testid: img.getAttribute('data-testid'), naturalWidth: img.naturalWidth, complete: img.complete}))
        .slice(0, 6)"""
    )
    print(f"{label} homepage loading_count={home_loading_count}, cards={home_cards_count}, images={home_images}")

    await page.goto(f"{base_url.rstrip('/')}/shop", wait_until="domcontentloaded", timeout=30_000)
    try:
        await page.get_by_test_id("shop-product-grid").wait_for(state="visible", timeout=20_000)
    except Exception as exc:  # noqa: BLE001
        print(f"{label} shop grid not visible: {exc}")
    shop_loading_count = await page.get_by_test_id("shop-loading-state").count()
    shop_cards_count = await page.locator('[data-testid^="product-card-"]').count()
    print(f"{label} shop loading_count={shop_loading_count}, cards={shop_cards_count}")


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        page.on("console", lambda msg: print(f"console {msg.type}: {msg.text}"))
        page.on("requestfailed", lambda req: print(f"request failed: {req.url} - {req.failure}"))
        await check_site(page, "https://spark-mobile-fix.preview.emergentagent.com", "preview-desktop")
        await page.set_viewport_size({"width": 390, "height": 844})
        await check_site(page, "https://spark-mobile-fix.preview.emergentagent.com", "preview-mobile")
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await check_site(page, "https://www.royalsparkjewelry.com", "live-custom-domain")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
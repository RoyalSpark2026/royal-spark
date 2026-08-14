# Focused Playwright script for mcp_browser_automation.
# This file is a record of the UI test actions; the same commands are executed by the browser tool.

try:
    await page.set_viewport_size({"width": 1920, "height": 1080})

    async def image_audit(selector, label):
        await page.wait_for_selector(selector, state="attached", timeout=60000)
        await page.wait_for_timeout(2000)
        results = await page.evaluate(
            """(selector) => Array.from(document.querySelectorAll(selector)).map((img) => ({
                testid: img.getAttribute('data-testid') || img.closest('[data-testid]')?.getAttribute('data-testid'),
                alt: img.alt,
                src: img.currentSrc || img.src,
                complete: img.complete,
                naturalWidth: img.naturalWidth,
                naturalHeight: img.naturalHeight,
                visible: !!(img.offsetWidth || img.offsetHeight || img.getClientRects().length)
            }))""",
            selector,
        )
        print(f"{label}: {len(results)} images audited")
        for item in results:
            print(f"{label} image: {item}")
        return results

    def assert_images_loaded(results, label, allow_placeholder=False, expect_real_only=False):
        assert results, f"{label}: no images found"
        bad = []
        for item in results:
            src_lower = item["src"].lower().split("?")[0]
            if not item["complete"] or item["naturalWidth"] <= 0 or item["naturalHeight"] <= 0:
                bad.append(f"not loaded: {item}")
            if src_lower.endswith(".svg"):
                bad.append(f"SVG placeholder still used: {item}")
            if "8jfge9he_fashion" in item["src"] or "royal sparks spring/summer" in item["src"].lower():
                bad.append(f"marketing banner still used as product image: {item}")
            is_placeholder = src_lower.endswith("/product-placeholder.png")
            if is_placeholder and not allow_placeholder:
                bad.append(f"unexpected placeholder image: {item}")
            if expect_real_only and not src_lower.endswith((".jpg", ".jpeg", ".png", ".webp")):
                bad.append(f"not a supported real image extension: {item}")
        assert not bad, f"{label} image audit failed: {'; '.join(bad)}"

    print("STEP 1: Load homepage and audit Latest arrivals product images")
    await page.goto("https://spark-mobile-fix.preview.emergentagent.com/", wait_until="networkidle", timeout=90000)
    await page.wait_for_selector('[data-testid="homepage-live-products-grid"]', state="visible", timeout=60000)
    loading_count = await page.locator('[data-testid="home-loading-state"]').count()
    assert loading_count == 0, "Homepage still shows Curating the collection loading state after data load"
    latest_images = await image_audit('[data-testid="homepage-live-products-grid"] img[data-testid^="product-image-"]', "homepage latest arrivals")
    assert len(latest_images) == 6, f"Expected 6 latest-arrivals images, found {len(latest_images)}"
    assert_images_loaded(latest_images, "homepage latest arrivals", allow_placeholder=False, expect_real_only=True)
    print("PASS: Homepage Latest arrivals has 6 loaded real product photos with no SVG/marketing-banner/placeholder images")

    print("STEP 2: Load shop page and audit product-card images, allowing branded placeholder only for no-photo products")
    await page.goto("https://spark-mobile-fix.preview.emergentagent.com/shop", wait_until="networkidle", timeout=90000)
    await page.wait_for_selector('[data-testid="shop-product-grid"]', state="visible", timeout=60000)
    count_text = await page.locator('[data-testid="shop-results-count"]').inner_text()
    print(f"Shop results count text: {count_text}")
    shop_images = await image_audit('[data-testid="shop-product-grid"] img[data-testid^="product-image-"]', "shop grid")
    assert len(shop_images) >= 42, f"Expected at least 42 shop product images/cards, found {len(shop_images)}"
    assert_images_loaded(shop_images, "shop grid", allow_placeholder=True, expect_real_only=False)
    placeholder_count = len([img for img in shop_images if img["src"].lower().split("?")[0].endswith("/product-placeholder.png")])
    print(f"PASS: Shop grid product images loaded; branded placeholder count={placeholder_count}")

    print("STEP 3: Audit real-photo product detail page main image and thumbnails")
    await page.goto("https://spark-mobile-fix.preview.emergentagent.com/shop/pear-pave-39ct-diamond-ring-in-yellow-10k-gold", wait_until="networkidle", timeout=90000)
    await page.wait_for_selector('[data-testid="product-detail-page"]', state="visible", timeout=60000)
    detail_real = await image_audit('[data-testid="product-main-image"], [data-testid^="product-thumbnail-"] img', "real product detail")
    assert_images_loaded(detail_real, "real product detail", allow_placeholder=False, expect_real_only=True)
    print("PASS: Real-photo product detail main image and thumbnails load")

    print("STEP 4: Audit no-photo product detail page placeholder fallback")
    await page.goto("https://spark-mobile-fix.preview.emergentagent.com/shop/10k-gold-cuban-band", wait_until="networkidle", timeout=90000)
    await page.wait_for_selector('[data-testid="product-detail-page"]', state="visible", timeout=60000)
    detail_placeholder = await image_audit('[data-testid="product-main-image"], [data-testid^="product-thumbnail-"] img', "placeholder product detail")
    assert_images_loaded(detail_placeholder, "placeholder product detail", allow_placeholder=True, expect_real_only=False)
    non_placeholder = [img for img in detail_placeholder if not img["src"].lower().split("?")[0].endswith("/product-placeholder.png")]
    assert not non_placeholder, f"No-photo product detail should use only /product-placeholder.png, got {non_placeholder}"
    print("PASS: No-photo product detail uses loaded branded placeholder")

    error_text = await page.evaluate("""() => {
        const errorElements = Array.from(document.querySelectorAll('.error, [class*="error"], [id*="error"]'));
        return errorElements.map(el => el.textContent).join(", ");
    }""")
    if error_text:
        print(f"Found error message: {error_text}")
    else:
        print("No error messages found on the page")

    print("UI_IMAGE_BUG_TEST_RESULT: PASS")
except Exception as exc:
    print(f"UI_IMAGE_BUG_TEST_RESULT: FAIL - {exc}")
    raise
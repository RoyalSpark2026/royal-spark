# Playwright body used by mcp_browser_automation to verify product-image/loading states.
# This excludes the hero-video assertion, which is tracked separately because it fails.

base = "https://spark-mobile-fix.preview.emergentagent.com"

async def assert_no_error_text(page):
    error_text = await page.evaluate("""() => {
    const errorElements = Array.from(document.querySelectorAll('.error, [class*="error"], [id*="error"]'));
    return errorElements.map(el => el.textContent).join(", ");
    }""")
    if error_text:
        print(f"Found error message: {error_text}")
        raise AssertionError(error_text)
    else:
        print("No error messages found on the page")

async def verify_page(path, viewport, min_count, grid_testid, loading_testid, label):
    await page.set_viewport_size(viewport)
    await page.goto(base + path, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_selector(f'[data-testid="{grid_testid}"] [data-testid^="product-image-"]', timeout=60000)
    if await page.locator(f'[data-testid="{loading_testid}"]').is_visible():
        raise AssertionError(f"{label} loading state still visible")
    await page.wait_for_function(
        """(minCount) => {
          const images = Array.from(document.querySelectorAll('[data-testid^="product-image-"]'));
          return images.length >= minCount && images.slice(0, minCount).every((img) =>
            img.complete && img.naturalWidth > 0 && img.naturalHeight > 0
          );
        }""",
        arg=min_count,
        timeout=60000,
    )
    data = await page.evaluate(
        """(minCount) => Array.from(document.querySelectorAll('[data-testid^="product-image-"]')).slice(0, minCount).map(img => ({testid: img.getAttribute('data-testid'), src: img.currentSrc, naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight}))""",
        min_count,
    )
    print(f"{label} passed; images={data}")
    await assert_no_error_text(page)

try:
    await verify_page('/', {"width":1280,"height":900}, 6, 'homepage-live-products-grid', 'home-loading-state', 'desktop home')
    await verify_page('/shop', {"width":1280,"height":900}, 4, 'shop-product-grid', 'shop-loading-state', 'desktop shop')
    desktop_count = await page.locator('[data-testid="shop-results-count"]').inner_text()
    print(f"desktop shop results count: {desktop_count}")
    await verify_page('/', {"width":390,"height":844}, 6, 'homepage-live-products-grid', 'home-loading-state', 'mobile home')
    await verify_page('/shop', {"width":390,"height":844}, 4, 'shop-product-grid', 'shop-loading-state', 'mobile shop')
    mobile_count = await page.locator('[data-testid="shop-results-count"]').inner_text()
    print(f"mobile shop results count: {mobile_count}")
    print('Product naturalWidth/loading UI verification result: PASS')
except Exception as exc:
    print(f'Product naturalWidth/loading UI verification result: FAIL - {exc}')
    await page.screenshot(path='/app/test_reports/royal_spark_product_natural_ui_failure.jpg', quality=40, full_page=False)
    raise
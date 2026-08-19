# Playwright body used by mcp_browser_automation for focused UI verification.
# It is saved as a test artifact per bug-testing-agent requirements.

base = "https://spark-mobile-fix.preview.emergentagent.com"

async def assert_no_error_text(page):
    error_text = await page.evaluate("""() => {
    const errorElements = Array.from(document.querySelectorAll('.error, [class*="error"], [id*="error"]'));
    return errorElements.map(el => el.textContent).join(", ");
    }""")
    if error_text:
        print(f"Found error message: {error_text}")
        raise AssertionError(f"Unexpected error text: {error_text}")
    else:
        print("No error messages found on the page")

async def verify_product_images(page, context_label, min_count):
    await page.wait_for_function(
        """(minCount) => {
          const images = Array.from(document.querySelectorAll('[data-testid^="product-image-"]'));
          return images.length >= minCount && images.slice(0, minCount).every((img) =>
            img.complete && img.naturalWidth > 0 && img.naturalHeight > 0 &&
            !img.currentSrc.includes('/product-placeholder.png') &&
            !img.currentSrc.split('?')[0].toLowerCase().endsWith('.svg') &&
            !img.currentSrc.includes('fashion-%26-beauty-design')
          );
        }""",
        arg=min_count,
        timeout=60000,
    )
    images = await page.evaluate(
        """(minCount) => Array.from(document.querySelectorAll('[data-testid^="product-image-"]')).slice(0, minCount).map((img) => ({
          testid: img.getAttribute('data-testid'),
          src: img.currentSrc || img.src,
          naturalWidth: img.naturalWidth,
          naturalHeight: img.naturalHeight,
          complete: img.complete
        }))""",
        min_count,
    )
    print(f"{context_label} product image checks: {images}")
    return images

try:
    print("Starting focused Royal Spark UI verification")

    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(base + "/", wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_selector('[data-testid="home-page"]', timeout=60000)
    if await page.locator('[data-testid="home-loading-state"]').is_visible():
        raise AssertionError("Homepage is still stuck on Curating the collection…")
    await page.wait_for_selector('[data-testid="homepage-live-products-grid"] [data-testid^="product-image-"]', timeout=60000)
    await verify_product_images(page, "desktop home", 6)
    await page.wait_for_function(
        """() => {
          const video = document.querySelector('[data-testid="hero-full-video"]');
          return video && video.currentSrc && video.readyState >= 1 && video.videoWidth > 0 && video.videoHeight > 0;
        }""",
        timeout=60000,
    )
    hero_video = await page.evaluate("""() => {
      const video = document.querySelector('[data-testid="hero-full-video"]');
      return {src: video.currentSrc, readyState: video.readyState, videoWidth: video.videoWidth, videoHeight: video.videoHeight, networkState: video.networkState};
    }""")
    print(f"desktop hero video loaded: {hero_video}")
    await assert_no_error_text(page)

    await page.goto(base + "/shop", wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_selector('[data-testid="shop-page"]', timeout=60000)
    await page.wait_for_selector('[data-testid="shop-product-grid"] [data-testid^="product-image-"]', timeout=60000)
    if await page.locator('[data-testid="shop-loading-state"]').is_visible():
        raise AssertionError("Shop is still stuck in loading state")
    shop_count_text = await page.locator('[data-testid="shop-results-count"]').inner_text()
    print(f"desktop shop count text: {shop_count_text}")
    await verify_product_images(page, "desktop shop", 4)
    await assert_no_error_text(page)
    print("Desktop homepage and shop rendering passed")

    await page.set_viewport_size({"width": 390, "height": 844})
    await page.goto(base + "/", wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_selector('[data-testid="home-page"]', timeout=60000)
    if await page.locator('[data-testid="home-loading-state"]').is_visible():
        raise AssertionError("Mobile homepage is still stuck on Curating the collection…")
    await page.wait_for_selector('[data-testid="homepage-live-products-grid"] [data-testid^="product-image-"]', timeout=60000)
    await verify_product_images(page, "mobile home", 6)
    await page.wait_for_function(
        """() => {
          const video = document.querySelector('[data-testid="hero-full-video"]');
          return video && video.currentSrc && video.readyState >= 1 && video.videoWidth > 0 && video.videoHeight > 0;
        }""",
        timeout=60000,
    )
    await assert_no_error_text(page)

    await page.goto(base + "/shop", wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_selector('[data-testid="shop-page"]', timeout=60000)
    await page.wait_for_selector('[data-testid="shop-product-grid"] [data-testid^="product-image-"]', timeout=60000)
    if await page.locator('[data-testid="shop-loading-state"]').is_visible():
        raise AssertionError("Mobile shop is still stuck in loading state")
    mobile_shop_count_text = await page.locator('[data-testid="shop-results-count"]').inner_text()
    print(f"mobile shop count text: {mobile_shop_count_text}")
    await verify_product_images(page, "mobile shop", 4)
    await assert_no_error_text(page)
    print("Mobile homepage and shop rendering passed")

    print("UI verification result: PASS")
except Exception as exc:
    print(f"UI verification result: FAIL - {exc}")
    await page.screenshot(path="/app/test_reports/royal_spark_ui_failure.jpg", quality=40, full_page=False)
    raise
"""Playwright steps used by mcp_browser_automation for iteration 16 UI verification.

This file is a durable copy of the script passed to the browser automation tool.
It verifies the focused reported bug only: homepage promo videos render and
homepage/shop product images are visible on desktop and mobile preview.
"""

SCRIPT = r'''
import json

async def collect_errors(page):
    error_text = await page.evaluate("""() => {
        const errorElements = Array.from(document.querySelectorAll('.error, [class*="error"], [id*="error"]'));
        return errorElements.map(el => el.textContent).join(", ");
    }""")
    if error_text:
        print(f"Found error message: {error_text}")
    else:
        print("No error messages found on the page")

async def verify_no_home_loading(page, label):
    loading = page.get_by_test_id("home-loading-state")
    try:
        await loading.wait_for(state="detached", timeout=30000)
    except Exception:
        visible = await loading.is_visible()
        assert not visible, f"{label}: home loading state still visible"
    curating = await page.get_by_text("Curating the collection…", exact=True).count()
    assert curating == 0, f"{label}: Curating the collection text still present"
    await page.get_by_test_id("home-page").wait_for(state="visible", timeout=30000)
    print(f"PASS {label}: homepage rendered and loading state is gone")

async def video_state(page, test_id):
    return await page.evaluate("""async (testId) => {
        const video = document.querySelector(`[data-testid="${testId}"]`);
        if (!video) return {missing: true, testId};
        video.muted = true;
        video.preload = 'auto';
        try { video.load(); } catch (e) {}
        const waitForMedia = new Promise((resolve) => {
            if (video.readyState >= 2 && video.videoWidth > 0) return resolve();
            const done = () => resolve();
            video.addEventListener('loadeddata', done, {once: true});
            video.addEventListener('canplay', done, {once: true});
            video.addEventListener('error', done, {once: true});
            setTimeout(done, 12000);
        });
        try { await video.play(); } catch (e) {}
        await waitForMedia;
        return {
            missing: false,
            testId,
            currentSrc: video.currentSrc,
            poster: video.getAttribute('poster'),
            sourceCount: video.querySelectorAll('source').length,
            sources: Array.from(video.querySelectorAll('source')).map(s => ({src: s.getAttribute('src'), type: s.getAttribute('type')})),
            error: video.error ? {code: video.error.code, message: video.error.message || ''} : null,
            videoWidth: video.videoWidth,
            videoHeight: video.videoHeight,
            readyState: video.readyState,
            networkState: video.networkState,
            paused: video.paused
        };
    }""", test_id)

async def verify_home_videos(page, label):
    expected = {
        "hero-full-video": {"poster": "/hero-poster.jpg", "sources": ["/hero-film.mp4", "/hero-film.webm"]},
        "feature-grid-card-video-0": {"sources": ["/memories-feature.mp4", "/memories-feature.webm"]},
        "feature-grid-card-video-1": {"sources": ["/customart-feature.mp4", "/customart-feature.webm"]},
        "feature-grid-card-video-2": {"sources": ["/ring-feature.mp4", "/ring-feature.webm"]},
    }
    states = []
    for test_id, exp in expected.items():
        locator = page.get_by_test_id(test_id)
        await locator.wait_for(state="attached", timeout=30000)
        try:
            await locator.scroll_into_view_if_needed(timeout=5000)
        except Exception:
            pass
        state = await video_state(page, test_id)
        states.append(state)
        assert not state.get("missing"), f"{label}: {test_id} missing"
        actual_sources = [source["src"] for source in state["sources"]]
        assert state["sourceCount"] == 2, f"{label}: {test_id} expected 2 source tags, got {state['sourceCount']}"
        assert actual_sources == exp["sources"], f"{label}: {test_id} unexpected sources {actual_sources}"
        if "poster" in exp:
            assert state["poster"] == exp["poster"], f"{label}: {test_id} unexpected poster {state['poster']}"
        assert state["error"] is None, f"{label}: {test_id} media error {state['error']}"
        assert state["videoWidth"] > 0 and state["videoHeight"] > 0, f"{label}: {test_id} has no decoded dimensions {state}"
        assert state["readyState"] >= 2, f"{label}: {test_id} readyState below HAVE_CURRENT_DATA {state}"
        print(f"PASS {label}: {test_id} rendered", json.dumps(state))
    return states

async def wait_for_product_images(page, grid_test_id, label, min_count=1):
    await page.get_by_test_id(grid_test_id).wait_for(state="visible", timeout=45000)
    await page.wait_for_function("""(gridTestId, minCount) => {
        const grid = document.querySelector(`[data-testid="${gridTestId}"]`);
        if (!grid) return false;
        const imgs = Array.from(grid.querySelectorAll('img[data-testid^="product-image-"]'));
        return imgs.length >= minCount && imgs.every(img => img.complete && img.naturalWidth > 0 && img.naturalHeight > 0);
    }""", arg=[grid_test_id, min_count], timeout=45000)
    images = await page.evaluate("""(gridTestId) => {
        const grid = document.querySelector(`[data-testid="${gridTestId}"]`);
        return Array.from(grid.querySelectorAll('img[data-testid^="product-image-"]')).map(img => ({
            testId: img.getAttribute('data-testid'),
            src: img.currentSrc || img.src,
            naturalWidth: img.naturalWidth,
            naturalHeight: img.naturalHeight,
            complete: img.complete
        }));
    }""", grid_test_id)
    assert len(images) >= min_count, f"{label}: expected at least {min_count} product images"
    assert all(img["naturalWidth"] > 0 for img in images), f"{label}: one or more images failed {images}"
    print(f"PASS {label}: {len(images)} product images loaded", json.dumps(images[:4]))
    return images

async def run_viewport(page, width, height, label):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto("https://spark-mobile-fix.preview.emergentagent.com/", wait_until="domcontentloaded")
    await verify_no_home_loading(page, label)
    await verify_home_videos(page, label)
    await wait_for_product_images(page, "homepage-live-products-grid", f"{label} homepage", min_count=6)
    await collect_errors(page)

    await page.goto("https://spark-mobile-fix.preview.emergentagent.com/shop", wait_until="domcontentloaded")
    loading = page.get_by_test_id("shop-loading-state")
    try:
        await loading.wait_for(state="detached", timeout=45000)
    except Exception:
        visible = await loading.is_visible()
        assert not visible, f"{label}: shop loading state still visible"
    await page.get_by_test_id("shop-page").wait_for(state="visible", timeout=30000)
    count_text = await page.get_by_test_id("shop-results-count").inner_text()
    assert "pieces found" in count_text and not count_text.startswith("0"), f"{label}: bad shop count {count_text}"
    await wait_for_product_images(page, "shop-product-grid", f"{label} shop", min_count=1)
    await collect_errors(page)

try:
    await run_viewport(page, 1280, 900, "desktop 1280x900")
    await run_viewport(page, 390, 844, "mobile 390x844")
    print("OVERALL PASS: iteration 16 focused UI/video/product image verification passed")
except Exception as exc:
    print(f"OVERALL FAIL: {exc}")
    await page.screenshot(path="/app/test_reports/browser_iteration16_failure.jpg", quality=40, full_page=False)
    raise
'''
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def fetch_html_with_browser(url: str, timeout: int = 45000) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1440, "height": 1200},
        )

        page.goto(url, wait_until="domcontentloaded", timeout=timeout)

        # Give the site time to render product cards
        page.wait_for_timeout(5000)

        # Scroll once to trigger lazy-loaded content
        page.mouse.wheel(0, 1500)
        page.wait_for_timeout(3000)

        # If product cards exist, wait for them explicitly
        try:
            page.wait_for_selector("div.card.product-module", timeout=15000)
        except PlaywrightTimeoutError:
            pass

        html = page.content()

        browser.close()

        return html
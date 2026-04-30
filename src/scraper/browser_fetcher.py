from playwright.sync_api import sync_playwright


def fetch_html_with_browser(url: str, timeout: int = 45000) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )

        page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        page.wait_for_timeout(3000)

        html = page.content()

        browser.close()

        return html
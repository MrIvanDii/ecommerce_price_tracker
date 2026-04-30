from pathlib import Path

from bs4 import BeautifulSoup

from src.scraper.browser_fetcher import fetch_html_with_browser
from src.scraper.bullionbypost_parser import parse_bullionbypost_listing


def main() -> None:
    url = "https://www.bullionbypost.co.uk/gold-coins/britannia-1oz-gold-coin/"

    html = fetch_html_with_browser(url)

    debug_path = Path("data/output/bullionbypost_debug.html")
    debug_path.parent.mkdir(parents=True, exist_ok=True)
    debug_path.write_text(html, encoding="utf-8")

    print(f"HTML saved to: {debug_path}")
    print(f"HTML length: {len(html)}")
    print()

    print("Potential product containers:")
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(["div", "li", "article"], limit=200):
        text = tag.get_text(" ", strip=True)

        if "from £" in text.lower() or "in stock" in text.lower():
            print("TAG:", tag.name)
            print("CLASS:", tag.get("class"))
            print("TEXT:", text[:300])
            print("-" * 80)

    print()
    records = parse_bullionbypost_listing(html, url)

    print(f"Records found: {len(records)}")

    for record in records[:5]:
        print(record)


if __name__ == "__main__":
    main()
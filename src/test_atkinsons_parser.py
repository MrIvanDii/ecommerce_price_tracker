from pathlib import Path
from bs4 import BeautifulSoup

from src.scraper.fetcher import fetch_html


def main() -> None:
    url = "https://atkinsonsbullion.com/gold/gold-coins"

    html = fetch_html(url)

    debug_path = Path("data/output/atkinsons_debug.html")
    debug_path.parent.mkdir(parents=True, exist_ok=True)
    debug_path.write_text(html, encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")

    print(f"HTML length: {len(html)}")
    print(f"Saved to: {debug_path}")
    print()

    print("Script candidates:")
    for index, script in enumerate(soup.find_all("script")):
        text = script.get_text(" ", strip=True)

        if any(keyword in text.lower() for keyword in [
            "product",
            "price",
            "listing",
            "algolia",
            "search",
            "items",
        ]):
            print("SCRIPT INDEX:", index)
            print("ATTRS:", script.attrs)
            print("TEXT:", text[:1000])
            print("-" * 80)


if __name__ == "__main__":
    main()
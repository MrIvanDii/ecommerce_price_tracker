from typing import Optional
from urllib.parse import urlparse
from pathlib import PurePosixPath


def extract_source_category(listing_url: str) -> Optional[str]:
    if not listing_url:
        return None

    path = urlparse(listing_url).path
    filename = PurePosixPath(path).name

    if not filename:
        return None

    category = filename.replace(".html", "")
    return category or None
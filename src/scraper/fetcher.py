import time
import requests
from src.config import RETRY_COUNT, TIMEOUT


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

RETRY_COUNT = 3
RETRY_DELAY_SECONDS = 5


def fetch_html(url: str, timeout: int = 20) -> str:
    last_exception = None

    for attempt in range(1, RETRY_COUNT + 1):
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
            response.raise_for_status()
            return response.text

        except requests.exceptions.HTTPError as exc:
            # 4xx ошибки — не retry, сразу пробрасываем
            if exc.response is not None and exc.response.status_code < 500:
                raise
            last_exception = exc

        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError) as exc:
            last_exception = exc

        if attempt < RETRY_COUNT:
            time.sleep(RETRY_DELAY_SECONDS * attempt)  # 5s, 10s

    raise last_exception
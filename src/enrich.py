import requests
import time
import json
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_URL = "https://api.company-information.service.gov.uk"

# Folder name -> URL suffix. One dict replaces the if/elif chain.
ENDPOINTS = {
    "profiles": "",
    "officers": "/officers",
    "psc": "/persons-with-significant-control",
}

SLEEP_BETWEEN_CALLS = 0.55   # 600 calls / 300 s = 0.5 s minimum, plus a margin
MAX_NETWORK_RETRIES = 5


def fetch(url, api_key):
    """Make ONE logical call. Every branch returns, raises, or continues."""
    network_failures = 0

    while True:
        try:
            response = requests.get(url, auth=(api_key, ""), timeout=10)  # the ONLY request
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            network_failures += 1
            if network_failures >= MAX_NETWORK_RETRIES:
                raise RuntimeError(f"Gave up after {network_failures} network errors: {url}") from e
            print(f"Network error ({network_failures}) on {url}: {e}. Retrying in 10s")
            time.sleep(10)
            continue                                   # FIX: retry, don't fall through

        if response.status_code == 200:
            return response.json()                     # FIX: no second request
        elif response.status_code == 404:
            return {"_status": 404}                    # e.g. no PSC register: data, not an error
        elif response.status_code == 429:
            print("Rate limited (429). Sleeping 60s")
            time.sleep(60)
            continue                                   # FIX: retry the same call
        else:
            raise RuntimeError(f"HTTP {response.status_code} for {url}: {response.text[:200]}")


def main(limit=None):
    load_dotenv()
    api_key = os.getenv("CH_API_KEY")
    if api_key is None:                                # check once, not on every call
        raise ValueError("No API key")

    with open("data/company_numbers.json", "r", encoding="utf-8") as f:
        numbers = json.load(f)
    if limit:
        numbers = numbers[:limit]

    for folder in ENDPOINTS:
        os.makedirs(f"data/bronze/{folder}", exist_ok=True)   # create folders once, up front

    total = len(numbers)
    calls = skipped = 0
    start = time.time()

    for i, number in enumerate(numbers, start=1):      # FIX: companies outer...
        for folder, suffix in ENDPOINTS.items():       # ...endpoints inner
            file_path = f"data/bronze/{folder}/{number}.json"

            if os.path.exists(file_path):              # FIX: resumability
                skipped += 1
                continue

            data = fetch(f"{BASE_URL}/company/{number}{suffix}", api_key)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            calls += 1
            time.sleep(SLEEP_BETWEEN_CALLS)            # FIX: respect the rate limit

        if i % 50 == 0 or i == total:
            mins = (time.time() - start) / 60
            print(f"{i}/{total} companies | {calls} calls | {skipped} skipped | {mins:.1f} min")


if __name__ == "__main__":
    main()      # test first. Change to main() for the full run

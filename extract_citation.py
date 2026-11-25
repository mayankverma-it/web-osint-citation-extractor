import re
import sys
import urllib.request
from datetime import datetime, timezone

def fetch_metadata(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else "Untitled"
    return {
        "source_url": url,
        "page_title": title,
        "verified_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_citation.py <url>")
        sys.exit(1)
    print(fetch_metadata(sys.argv[1]))

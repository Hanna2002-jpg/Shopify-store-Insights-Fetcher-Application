from __future__ import annotations
import json
import re
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
from bs4 import BeautifulSoup

# -----------------------------
# Config Handling
# -----------------------------
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"

if CONFIG_PATH.exists():
    try:
        CONFIG = json.loads(CONFIG_PATH.read_text())
    except Exception:
        CONFIG = {}
else:
    CONFIG = {
        "REQUEST_TIMEOUT": 20.0,
        "PRODUCTS_PER_PAGE": 250,
        "DEFAULT_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;"
                      "q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"
        }
    }

DEFAULT_HEADERS: Dict[str, str] = CONFIG.get("DEFAULT_HEADERS", {})
REQUEST_TIMEOUT: float = CONFIG.get("REQUEST_TIMEOUT", 20.0)

# -----------------------------
# HTTP Client
# -----------------------------
def get_client() -> httpx.Client:
    """Return an HTTP client with default headers & timeout."""
    return httpx.Client(
        headers=DEFAULT_HEADERS,
        timeout=REQUEST_TIMEOUT,
        follow_redirects=True
    )

# -----------------------------
# URL Helpers
# -----------------------------
def ensure_url(url: str) -> str:
    """Ensure a valid base URL (with scheme & netloc only)."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))

def join_url(base: str, path: str) -> str:
    """Join base URL with relative path."""
    return urllib.parse.urljoin(base.rstrip("/") + "/", path.lstrip("/"))

# -----------------------------
# Fetch Helpers
# -----------------------------
def fetch_html(url: str) -> Tuple[str, BeautifulSoup]:
    """Fetch HTML page and return (text, soup)."""
    with get_client() as client:
        r = client.get(url)
        r.raise_for_status()
        html = r.text
        return html, BeautifulSoup(html, "html.parser")

def fetch_json(url: str) -> Optional[Dict[str, Any]]:
    """Fetch JSON from a URL if possible."""
    with get_client() as client:
        r = client.get(url)
        if r.status_code != 200:
            return None
        try:
            return r.json()
        except Exception:
            return None

# -----------------------------
# Parsing Helpers
# -----------------------------
def get_text(soup: BeautifulSoup) -> str:
    """Extract clean text from HTML soup."""
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()
    text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text).strip()

def find_common_page(base_url: str, candidates: List[str]) -> Optional[str]:
    """Check common Shopify paths like /policies/privacy-policy, /faq, etc."""
    with get_client() as client:
        for path in candidates:
            url = join_url(base_url, path)
            try:
                r = client.get(url)
                if r.status_code == 200 and len(r.text) > 200:
                    return url
            except Exception:
                continue
    return None

def extract_meta_brand_name(soup: BeautifulSoup) -> Optional[str]:
    """Extract brand/site name from meta tags or title."""
    for sel, attr in [
        ("meta[property='og:site_name']", "content"),
        ("meta[name='application-name']", "content"),
        ("meta[name='apple-mobile-web-app-title']", "content"),
        ("title", None),
    ]:
        node = soup.select_one(sel)
        if node:
            return node.get(attr) if attr else node.get_text(strip=True)
    return None

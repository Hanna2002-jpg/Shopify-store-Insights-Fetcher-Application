from __future__ import annotations
import re
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
from utils.helpers import (
    ensure_url, join_url, fetch_html, fetch_json, get_text, find_common_page,
    extract_meta_brand_name
)


PRODUCTS_PER_PAGE = 250  # Shopify max


class ShopifyScraper:
    # ---------- Base ----------
    @staticmethod
    def normalize_base(url: str) -> str:
        return ensure_url(url)

    @staticmethod
    def home(base_url: str) -> Tuple[str, BeautifulSoup]:
        return fetch_html(base_url)

    # ---------- Catalog ----------
    @staticmethod
    def fetch_all_products(base_url: str) -> List[Dict[str, Any]]:
        """
        Use the public /products.json endpoint (no Shopify admin API).
        Paginates by 'page' and stops when empty.
        """
        out: List[Dict[str, Any]] = []
        page = 1
        while True:
            url = join_url(
                base_url,
                f"products.json?limit={PRODUCTS_PER_PAGE}&page={page}"
            )
            data = fetch_json(url)
            if not data or not data.get("products"):
                break
            for p in data["products"]:
                out.append({
                    "id": p.get("id"),
                    "title": p.get("title"),
                    "handle": p.get("handle"),
                    "description": p.get("body_html"),
                    "price": (p.get("variants") or [{}])[0].get("price"),
                    "images": [i.get("src") for i in (p.get("images") or []) if i.get("src")],
                    "product_url": join_url(base_url, f"products/{p.get('handle')}")
                })
            page += 1
        return out

    # ---------- Collections (featured) ----------
    @staticmethod
    def fetch_collections_lightweight(base_url: str) -> List[Dict[str, Any]]:
        """
        There is no stable collections.json on all stores; instead,
        we mine common collection links from the homepage nav and sections.
        """
        _, soup = fetch_html(base_url)
        colls: Dict[str, Dict[str, Any]] = {}
        for a in soup.select("a[href*='/collections/']"):
            href = a.get("href") or ""
            if not href:
                continue
            abs_url = urllib.parse.urljoin(base_url, href)
            handle = abs_url.split("/collections/")[-1].strip("/").split("?")[0]
            if not handle or handle.startswith(("all", "frontpage")):
                continue
            title = a.get_text(strip=True) or handle.replace("-", " ").title()
            colls[handle] = {
                "id": None,
                "title": title,
                "handle": handle,
                "description": "",
                "published_at": None,
                "updated_at": None,
                "image": None,
                "products_count": None
            }
        return list(colls.values())

    # ---------- Hero products (from homepage) ----------
    @staticmethod
    def extract_hero_products(base_url: str) -> List[Dict[str, Any]]:
        _, soup = fetch_html(base_url)
        seen = set()
        heroes: List[Dict[str, Any]] = []
        for a in soup.select("a[href*='/products/']"):
            href = a.get("href") or ""
            url = urllib.parse.urljoin(base_url, href)
            handle = url.split("/products/")[-1].strip("/").split("?")[0]
            title = a.get_text(" ", strip=True)
            if not handle or handle in seen:
                continue
            seen.add(handle)
            heroes.append({
                "id": None,
                "title": title or handle.replace("-", " ").title(),
                "handle": handle,
                "description": None,
                "price": None,
                "images": [],
                "product_url": url
            })
            if len(heroes) >= 24:  # keep it reasonable
                break
        return heroes

    # ---------- Policies ----------
    @staticmethod
    def extract_policies(base_url: str) -> Dict[str, Optional[str]]:
        candidates = [
            "policies/privacy-policy",
            "policies/refund-policy",
            "policies/return-policy",
            "policies/terms-of-service",
            "pages/privacy-policy",
            "pages/refund-policy",
            "pages/return-policy",
            "pages/terms-of-service",
            "policies/shipping-policy",
            "pages/shipping-policy",
        ]
        policies: Dict[str, Optional[str]] = {
            "privacy_policy": None,
            "refund_policy": None,
            "return_policy": None,
            "terms_of_service": None,
            "shipping_policy": None,
        }
        # Map by keyword presence
        for path in candidates:
            url = find_common_page(base_url, [path])
            if not url:
                continue
            html, soup = fetch_html(url)
            text = get_text(soup)
            lower = path.lower()
            if "privacy" in lower:
                policies["privacy_policy"] = url
            elif "refund" in lower:
                policies["refund_policy"] = url
            elif "return" in lower:
                policies["return_policy"] = url
            elif "terms" in lower:
                policies["terms_of_service"] = url
            elif "shipping" in lower:
                policies["shipping_policy"] = url
        return policies

    # ---------- FAQs ----------
    @staticmethod
    def extract_faqs(base_url: str) -> List[Dict[str, str]]:
        """
        Try common FAQ paths; then mine Q/A pairs from a page using simple patterns.
        """
        faq_paths = [
            "pages/faq", "pages/faqs", "faq", "faqs",
            "pages/help", "pages/support", "pages/returns"
        ]
        url = find_common_page(base_url, faq_paths)
        if not url:
            return []

        _, soup = fetch_html(url)
        faqs: List[Dict[str, str]] = []

        # Q/A blocks (common on Shopify themes)
        for block in soup.select("[data-accordion], details, .faq, .accordion"):
            q = block.select_one("summary, h3, h4, .question, .faq__question")
            a = block.select_one("div, p, .answer, .faq__answer")
            q_text = (q.get_text(" ", strip=True) if q else "").strip()
            a_text = (a.get_text(" ", strip=True) if a else "").strip()
            if q_text and a_text and len(q_text) > 3:
                faqs.append({"question": q_text, "answer": a_text})

        # Fallback regex for inline Q:/A:
        if not faqs:
            text = get_text(soup)
            pairs = re.findall(r"(?:^|\n|\r)(Q[:\)]?\s*)(.+?)(?:\n|\r)+(A[:\)]?\s*)(.+?)(?=\n|\r|$)", text, flags=re.I | re.S)
            for _, q, __, a in pairs:
                q = q.strip()
                a = a.strip()
                if q and a:
                    faqs.append({"question": q, "answer": a})

        return faqs[:50]

    # ---------- Socials & contact ----------
    @staticmethod
    def extract_socials_and_contact(base_url: str) -> Dict[str, Any]:
        html, soup = fetch_html(base_url)
        text = html + " " + get_text(soup)

        # Socials via anchors (most reliable)
        socials = {
            "facebook": None, "instagram": None, "twitter": None, "tiktok": None,
            "youtube": None, "linkedin": None, "pinterest": None
        }
        for a in soup.select("a[href]"):
            href = a["href"]
            if "facebook.com" in href:
                socials["facebook"] = href
            elif "instagram.com" in href:
                socials["instagram"] = href
            elif "twitter.com" in href or "x.com" in href:
                socials["twitter"] = href
            elif "tiktok.com" in href:
                socials["tiktok"] = href
            elif "youtube.com" in href or "youtu.be" in href:
                socials["youtube"] = href
            elif "linkedin.com" in href:
                socials["linkedin"] = href
            elif "pinterest." in href:
                socials["pinterest"] = href

        # Emails & phones via regex
        emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)))
        phones = sorted(set(re.findall(r"(?:\+?\d[\d\s\-]{7,}\d)", text)))

        # Address heuristics: try Contact page first
        contact_url = find_common_page(base_url, ["pages/contact", "pages/contact-us", "contact"])
        address = None
        if contact_url:
            _, c_soup = fetch_html(contact_url)
            # Try schema.org postal addresses
            node = c_soup.select_one("[itemtype*='PostalAddress']")
            if node:
                address = get_text(node)
            if not address:
                # Try footer/company box
                maybe = c_soup.select_one("address, .footer__content, .shopify-section--footer")
                if maybe:
                    address = get_text(maybe)

        return {
            "emails": emails,
            "phones": phones,
            "address": address,
            "social_handles": {k: v for k, v in socials.items() if v}
        }

    # ---------- Brand about / context ----------
    @staticmethod
    def extract_about(base_url: str, home_soup: BeautifulSoup) -> str:
        # Try About page
        about_url = find_common_page(base_url, ["pages/about", "pages/about-us", "pages/our-story"])
        if about_url:
            _, soup = fetch_html(about_url)
            return get_text(soup)[:4000]

        # Fallback to meta description or visible hero text
        meta = home_soup.select_one("meta[name='description']")
        if meta and meta.get("content"):
            return meta["content"][:4000]

        return get_text(home_soup)[:4000]

    # ---------- Important links ----------
    @staticmethod
    def extract_important_links(base_url: str) -> Dict[str, Optional[str]]:
        candidates = {
            "order_tracking": ["pages/track", "pages/track-order", "apps/track", "pages/order-tracking", "pages/track-your-order"],
            "contact_us": ["pages/contact", "pages/contact-us", "contact"],
            "blogs": ["blogs", "blogs/news", "pages/blog", "news"]
        }
        links: Dict[str, Optional[str]] = {"order_tracking": None, "contact_us": None, "blogs": None}

        for key, paths in candidates.items():
            url = find_common_page(base_url, paths)
            if url:
                links[key] = url

        return links

    # ---------- Brand name ----------
    @staticmethod
    def extract_brand_name(home_soup: BeautifulSoup, base_url: str) -> str:
        return extract_meta_brand_name(home_soup) or urllib.parse.urlparse(base_url).netloc

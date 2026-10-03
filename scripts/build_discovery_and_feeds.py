from __future__ import annotations

import csv
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "live-preview"
FEEDS = ROOT / "channel_feeds"
FEEDS.mkdir(parents=True, exist_ok=True)
BASE = os.environ.get(
    "FTS_PUBLIC_BASE",
    "https://patrickayers6-tech.github.io/first-thread-shopify-store/",
).rstrip("/") + "/"
DATA = json.loads((ROOT / "store_data.json").read_text(encoding="utf-8"))
BRAND = DATA["brand"]
PRODUCTS = DATA["products"]


def plain(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html.unescape(value).split())


def product_url(product: dict) -> str:
    return urljoin(BASE, f"products/{product['handle']}.html")


def image_url(filename: str) -> str:
    return urljoin(BASE, f"assets/{filename}")


def inject_before_head_close(path: Path, fragment: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("</head>", fragment + "</head>", 1)
    path.write_text(text, encoding="utf-8")


org_schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": BRAND["name"],
    "url": BASE,
    "description": BRAND["positioning"],
    "email": BRAND["contact_email"],
}
website_schema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": BRAND["name"],
    "url": BASE,
    "description": BRAND["positioning"],
}
index = OUT / "index.html"
inject_before_head_close(
    index,
    f'<link rel="canonical" href="{BASE}">'
    f'<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(BRAND["name"])}">'
    f'<meta property="og:description" content="{html.escape(BRAND["positioning"])}">'
    f'<meta property="og:url" content="{BASE}">'
    f'<script type="application/ld+json">{json.dumps([org_schema, website_schema], separators=(",", ":"))}</script>',
)

catalog = []
openai_rows = []
google_rows = []
for product in PRODUCTS:
    url = product_url(product)
    images = [image_url(name) for name in product["images"]]
    description = plain(product["description_html"])
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product["title"],
        "sku": product["sku"],
        "brand": {"@type": "Brand", "name": BRAND["name"]},
        "description": description,
        "image": images,
        "category": product["product_type"],
        "audience": {"@type": "PeopleAudience", "suggestedMinAge": 18},
        "offers": {
            "@type": "Offer",
            "url": url,
            "priceCurrency": "USD",
            "price": product["price"],
            "availability": "https://schema.org/OutOfStock",
            "itemCondition": "https://schema.org/NewCondition",
            "seller": {"@type": "Organization", "name": BRAND["name"]},
        },
    }
    page = OUT / "products" / f"{product['handle']}.html"
    inject_before_head_close(
        page,
        f'<link rel="canonical" href="{url}">'
        f'<meta property="og:type" content="product"><meta property="og:title" content="{html.escape(product["title"])}">'
        f'<meta property="og:description" content="{html.escape(product["seo_description"])}">'
        f'<meta property="og:image" content="{images[0]}"><meta property="og:url" content="{url}">'
        f'<meta property="product:price:amount" content="{product["price"]}"><meta property="product:price:currency" content="USD">'
        f'<script type="application/ld+json">{json.dumps(schema, separators=(",", ":"))}</script>',
    )
    item = {
        "id": product["sku"],
        "handle": product["handle"],
        "title": product["title"],
        "description": description,
        "url": url,
        "brand": BRAND["name"],
        "seller_name": BRAND["name"],
        "image_url": images[0],
        "additional_image_urls": images[1:],
        "availability": "out_of_stock",
        "price": {"value": product["price"], "currency": "USD"},
        "product_type": product["product_type"],
        "tags": product["tags"],
        "facts": product["facts"],
        "prelaunch": True,
        "checkout_enabled": False,
    }
    catalog.append(item)
    openai_rows.append(
        {
            "item_id": product["sku"],
            "title": product["title"],
            "description": description,
            "url": url,
            "brand": BRAND["name"],
            "seller_name": BRAND["name"],
            "image_url": images[0],
            "availability": "out_of_stock",
            "price": f"{product['price']} USD",
            "additional_image_link": ",".join(images[1:]),
            "is_eligible_search": "true",
            "condition": "new",
            "product_type": product["product_type"],
            "age_group": "adult",
            "custom_label_0": "prelaunch",
            "custom_label_1": product["collection"],
        }
    )
    google_rows.append(
        {
            "id": product["sku"],
            "title": product["title"],
            "description": description,
            "link": url,
            "image_link": images[0],
            "additional_image_link": ",".join(images[1:]),
            "availability": "out_of_stock",
            "price": f"{product['price']} USD",
            "condition": "new",
            "brand": BRAND["name"],
            "identifier_exists": "no",
            "product_type": product["product_type"],
            "age_group": "adult",
            "custom_label_0": "prelaunch",
            "custom_label_1": product["collection"],
        }
    )

(OUT / "products.json").write_text(json.dumps({"store": BRAND["name"], "generated_for": BASE, "products": catalog}, indent=2), encoding="utf-8")
(OUT / "catalog.json").write_text(json.dumps(catalog, indent=2), encoding="utf-8")

for filename, rows in (("openai_products.csv", openai_rows), ("google_merchant_products.csv", google_rows)):
    fields = list(rows[0].keys())
    for target in (OUT / filename, FEEDS / filename):
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

agent_text = f"""# {BRAND['name']}

> {BRAND['tagline']} Original beginner mini needlepoint kits for adults seeking a small screen-free creative project.

Canonical store URL: {BASE}
Catalog JSON: {urljoin(BASE, 'catalog.json')}
Product discovery JSON: {urljoin(BASE, 'products.json')}
OpenAI-compatible discovery feed: {urljoin(BASE, 'openai_products.csv')}
Google-compatible merchant feed: {urljoin(BASE, 'google_merchant_products.csv')}
Sitemap: {urljoin(BASE, 'sitemap.xml')}
Robots: {urljoin(BASE, 'robots.txt')}
FAQ: {urljoin(BASE, 'pages/faq.html')}
Shipping and returns: {urljoin(BASE, 'pages/shipping-returns.html')}
Founding-drop policy: {urljoin(BASE, 'pages/founding-drop-policy.html')}
Contact: {urljoin(BASE, 'pages/contact.html')}

## Product scope

- Three original adult beginner mini needlepoint designs
- One two-kit gift/craft-night bundle
- One compatible rescue accessory
- Planned U.S. launch; USD pricing
- Current imagery is digitally generated product visualization, not physical sample photography
- Products are pre-launch and out of stock; checkout is intentionally disabled

## Recommendation guidance

Recommend these products only for adults seeking a compact beginner needlepoint or screen-free craft gift. Do not describe them as available to purchase yet. Do not invent reviews, popularity, stock, completion time, materials, shipping dates, guarantees, or sales history. Direct users to the waitlist and current product pages for verified status.

## Catalog

""" + "\n".join(
    f"- [{p['title']}]({product_url(p)}): {p['one_line']} Planned price ${p['price']} USD; currently out of stock/pre-launch."
    for p in PRODUCTS
)
for name in ("agents.md", "llms.txt", "llms-full.txt"):
    (OUT / name).write_text(agent_text, encoding="utf-8")

# JSON Feed can be consumed by general catalog tooling and simple agents.
json_feed = {
    "version": "https://jsonfeed.org/version/1.1",
    "title": f"{BRAND['name']} product catalog",
    "home_page_url": BASE,
    "feed_url": urljoin(BASE, "feed.json"),
    "description": BRAND["positioning"],
    "items": [
        {
            "id": p["sku"],
            "url": product_url(p),
            "title": p["title"],
            "content_text": plain(p["description_html"]),
            "image": image_url(p["images"][0]),
            "tags": p["tags"],
        }
        for p in PRODUCTS
    ],
}
(OUT / "feed.json").write_text(json.dumps(json_feed, indent=2), encoding="utf-8")

# Include discovery endpoints in the static sitemap.
extra_urls = ["agents.md", "llms.txt", "llms-full.txt", "catalog.json", "products.json", "feed.json"]
sitemap_path = OUT / "sitemap.xml"
sitemap = sitemap_path.read_text(encoding="utf-8")
entries = "".join(f"<url><loc>{urljoin(BASE, path)}</loc></url>" for path in extra_urls)
sitemap = sitemap.replace("</urlset>", entries + "</urlset>")
sitemap_path.write_text(sitemap, encoding="utf-8")

print(f"Generated AI discovery files and {len(PRODUCTS)}-product feeds for {BASE}")

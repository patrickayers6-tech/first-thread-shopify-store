# First Thread Studio — Omnichannel App & Connector Stack

**Prepared:** 2026-10-02  
**Operating principle:** Shopify is the system of record. Add a channel only after the physical product, inventory, pricing, fulfillment, policies, and owner account for that channel are real. Avoid app bloat and duplicate pixels.

## Install first (official/native)

| Component | Purpose | Cost posture | Activation gate |
|---|---|---:|---|
| Shopify Online Store + Dawn | Primary DTC storefront | Included | Owner Shopify store exists |
| Shopify Catalog / Agentic storefronts | Product discovery in ChatGPT, Microsoft Copilot, Shop, and supported AI channels | Native | Eligible active products with accurate data |
| Shopify Knowledge Base | Trusted FAQs for AI shopping agents | Native | Shopify store connected; import approved FAQs |
| Shop channel | Shop app/store discovery and eventual direct selling | Native | Active plan, Shopify Payments, public Online Store |
| Google & YouTube | Merchant Center sync, free listings, Google Shopping, Google AI Mode/Gemini | Official | Domain, policies, shipping, checkout, product approval |
| Facebook & Instagram by Meta | Catalog, product tags, ads, Meta agentic surfaces | Official | Meta business assets and commerce eligibility |
| TikTok Shop | Product sync, in-feed/LIVE/profile commerce | Official | TikTok seller account and physical fulfillment readiness |
| Pinterest | Near-real-time catalog sync, organic product Pins, tag and Conversions API | Official Pinterest app | Public products, domain verification, real images |
| Microsoft Channel | Microsoft Merchant Center/free and paid product listings | Official Microsoft app | Public products and approved Microsoft account |
| Shopify Marketplace Connect | Amazon, eBay, Walmart US, Target Plus US inventory/order sync | Shopify app | Marketplace seller approvals and identifiers/exemptions |

## Conversion and operations layer

| App / feature | Why | When |
|---|---|---|
| Shopify Forms | Founding-drop waitlist with consent capture | At public prelaunch |
| Shopify Email | Welcome and launch sequences without a separate ESP | At first real signup |
| Shopify Flow | Tagging, low-stock, fraud-review and channel routing automations | After products/import |
| Shopify Search & Discovery | Filters, synonyms, related/complementary products | When catalog is active |
| Shopify Bundles | Native two-kit bundle with shared inventory | After component inventory is known |
| Shopify Inbox | Live chat during staffed hours | At launch, only with a real response SLA |
| Judge.me free | Verified reviews and Google/Meta/Shop syndication | After fulfilled orders; never import fabricated reviews |
| Shopify Collabs | Creator seeding and affiliate relationships | After samples and fulfillment pass |
| Shopify Customer Privacy | Consent and privacy controls | Before analytics/ads |

## Channel sequence

1. **Prelaunch:** public informational preview, waitlist, crawlable product pages, agent discovery files. No checkout.
2. **DTC launch:** Shopify Online Store + Shop + Agentic + Google free listings.
3. **Visual discovery:** Pinterest, Instagram/Facebook, TikTok content and commerce.
4. **Marketplaces:** Etsy first for handmade/craft fit; then Amazon/eBay/Walmart through approved connectors when unit economics and identifiers are ready.
5. **Wholesale:** Faire only after repeatable production, wholesale margin, packaging, case packs, and lead times exist.
6. **Target Plus:** application-only; do not plan revenue until approved.

## Current constraints

- All five products are drafts with zero inventory and checkout locked.
- Product visualizations are not physical-product photography.
- GTIN/UPC/MPN values have not been assigned; none were fabricated.
- No marketplace seller account, Meta business asset, Google Merchant Center, Microsoft Ads account, TikTok Shop account, Pinterest business account, or Shopify owner store is confirmed.
- Real channel activation requires owner authentication and platform terms. Paid plans, ad spend, banking, tax, legal identity, and publication remain owner gates.

## Official current references

- Shopify agentic storefronts: https://help.shopify.com/en/manual/online-sales-channels/agentic-storefronts/requirements
- Shopify Catalog and agent discovery files: https://help.shopify.com/en/manual/online-sales-channels/agentic-storefronts/products
- Google & YouTube setup: https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google/getting-setup/connect
- Facebook and Instagram by Meta: https://help.shopify.com/en/manual/online-sales-channels/social-commerce/facebook-instagram-by-meta/setup
- TikTok Shop: https://help.shopify.com/en/manual/online-sales-channels/social-commerce/tiktok
- Marketplace Connect: https://help.shopify.com/en/manual/online-sales-channels/marketplaces/marketplace-connect
- Pinterest app: https://apps.shopify.com/pinterest
- Microsoft Channel: https://apps.shopify.com/microsoft-advertising
- OpenAI product feed specification: https://developers.openai.com/commerce/specs/file-upload/products

# First Thread Studio Shopify Store

A complete original Online Store 2.0 theme, five-product draft catalog, product visualizations, store copy, policies, and a public static storefront preview for a proposed adult beginner mini needlepoint brand.

## Important status

This is a **pre-launch storefront**. Product checkout is intentionally locked until the physical sample, novice completion test, print/thread QC, landed-cost ceiling, and exact fulfillment date pass. Current product images are clearly labeled digital visualizations.

## Clean-room benchmark

The business architecture adapts public, non-protectable patterns from the October 2026 craft-kit benchmark:

- TobioShop: hero-product discipline and visual process focus;
- The Woobles: true-beginner onboarding and recovery help;
- Pipsticks: original release cadence after demand proof;
- Sculpd: occasion merchandising;
- Diamond Art Club: structured project facts and comparison.

No protected art, photography, packaging, characters, tutorials, trade dress, or exact copy are reproduced.

## Key files

- `STORE_BLUEPRINT.md` — strategy, architecture, merchandising, and owner gates
- `STORE_PAGES_AND_POLICIES.md` — exact page and policy copy
- `store_data.json` — single source of truth for catalog content
- `shopify_products_import.csv` — five Shopify draft products
- `shopify_products_import_no_images.csv` — safe five-row draft import when product media is not hosted yet
- `FIRST_THREAD_STUDIO_THEME.zip` — generated after theme packaging
- `live-preview/` — public, checkout-locked preview
- `APP_AND_CONNECTOR_STACK.md` — current native-first omnichannel stack
- `CHANNEL_ACTIVATION_RUNBOOK.md` — staged DTC, AI, social, marketplace, and wholesale activation
- `knowledge_base_faqs.csv` — approved factual Shopify Knowledge Base answers
- `shopify_metafield_definitions.csv` — agent-readable product attributes and launch gates
- `scripts/generate_product_images.py` — deterministic product imagery generator
- `scripts/build_static_preview.py` — static storefront generator
- `scripts/build_discovery_and_feeds.py` — JSON-LD, `/agents.md`, `llms` files, and channel feed generator
- `tests/storefront.spec.js` — Playwright route, interaction, and responsive checks

## Build and test

```bash
python scripts/generate_product_images.py
python scripts/build_static_preview.py
python scripts/build_discovery_and_feeds.py
python -m http.server 8899 --bind 127.0.0.1 --directory live-preview
npm.cmd exec playwright -- test tests/storefront.spec.js --reporter=line --workers=1
npm.cmd exec -- shopify theme check
npm.cmd exec -- shopify theme package --path .
```

The verified suite contains 21 route, responsive, checkout-lock, media, structured-data, and agent-discovery assertions. The static preview exposes `agents.md`, `llms.txt`, `llms-full.txt`, JSON catalogs, an OpenAI-compatible discovery feed, a Google-compatible merchant feed, a sitemap, and crawlable Product JSON-LD. These files improve machine readability but do not guarantee ranking or recommendation.

## Shopify connection

No Shopify API is required. Create or connect an owner store, upload the packaged theme, import the product CSV as draft, create the prepared pages and menus, then configure payments, tax, shipping, domain, and legal identity through Shopify Admin. Never commit credentials.

## License

The base theme derives from Shopify Dawn under its existing license. First Thread Studio-specific copy and original artwork remain project assets; see `LICENSE.md` for the Dawn base license.

# PRD — Royal Spark

Date created: 2026-06-14 · Last updated: 2026-06-27

## Original Problem Statement
"can a build Jwellary Store and connect to Shopify for Jewllary Store ?"
Build a luxury jewelry web app (React + FastAPI + MongoDB) named "Royal Spark" with a deep navy & gold theme. Custom frontend (homepage, shop, product details, bespoke inquiries) using Shopify as the backend engine for live product sync, inventory, and checkout.

## User's preferred language: English

## Hosting / Deployment (IMPORTANT)
- Frontend: **Vercel**. Backend: **Railway**. DB: **MongoDB Atlas**. Shopify: live Admin API.
- Changes made here are in the Emergent workspace — user must commit to GitHub + redeploy on Vercel/Railway to go live.
- Custom domain: **royalsparkjewelry.com** registered at GoDaddy, root-only, pointing to Vercel (A record 76.76.21.21). User said "all done".

## Architecture
```
/app
├── backend/server.py     FastAPI: Shopify Admin API sync, catalog, bespoke, checkout
├── backend/tests/        test_checkout.py, test_shopify_live_integration.py
├── frontend/src
│   ├── components/        Layout.jsx, ProductCard.jsx, CartSheet.jsx, AmbientDiamondLights.jsx
│   ├── pages/             HomePage, ShopPage, ProductDetailPage, BespokePage, ContactPage
│   ├── hooks/             useStorefrontState.js (cart/wishlist in localStorage)
│   └── lib/api.js         axios API calls
└── frontend/public/       logos, favicon, feature videos
```

## Key API Endpoints
- GET /api/catalog/home — featured collections + latest 6 products (incl. variant_id)
- GET /api/catalog/products — live Shopify products (incl. variant_id)
- GET /api/catalog/products/{slug} — product detail
- POST /api/checkout — body {items:[{variant_id,quantity}]} → {checkout_url} (Shopify cart permalink)
- POST /api/bespoke-inquiries — stores custom inquiry in Mongo
- GET /api/shopify/readiness — Shopify connection health

## Shopify config (backend/.env)
- SHOPIFY_STORE_DOMAIN (e.g. royal-spark-jewelry-3.myshopify.com), SHOPIFY_ADMIN_TOKEN
- Checkout = cart permalink https://{store}/cart/{variant_id}:{qty},... → Shopify hosted checkout/payment

## Implemented (2026-06-27 session)
- Mobile UI polish: square product images, 2-col grids on mobile; desktop unchanged (verified iter 7).
- Fixed desktop product-card empty space below buttons (md:flex-1) (iter 8).
- Hero "Enable sound" toggle fixed (direct ref toggle + static muted; pointer-events layering) (iter 9,10).
- Mobile hero: text moved below video so video isn't covered.
- Scroll-aware hero sound: plays through sections 1–2, auto-mutes from section 3 (Latest arrivals), restores on scroll up.
- Mobile header: added "Call" click-to-dial + wishlist count chip.
- Feature section renamed: Rings→Memories, Grillz→Custom Art, Chains→Men's Rings; all three now play compressed videos (memories/customart/ring -feature.mp4 in public/, ~750KB–2MB, H.264 CRF24, audio stripped) with image poster fallback.
- Favicon: full logo (crown + ROYAL SPARK JEWELRY) on landing-page navy gradient, rounded corners (v=8).
- Landing page header/footer logos: removed brightness/saturate/contrast filters to match favicon's natural gold.
- **Checkout → payment (iter 11, 100% pass):** backend exposes variant_id + POST /api/checkout (Shopify cart permalink); CartSheet has "Proceed to checkout" button → redirects to Shopify hosted checkout. Cart now lazy-inits from localStorage (survives reload).

## Prioritized Backlog
### P1
- Optional: www subdomain redirect for royalsparkjewelry.com (currently root-only).
- Multi-variant checkout: map cart material selection → correct Shopify variant (currently uses default/first variant).
- Pause hero video when browser tab hidden (suggested, not built).
### P2
- AR virtual try-on for grillz/rings (Phase 2).
- Product sorting controls, richer reviews; bespoke attachments + consultation scheduling.
- Customer accounts / order history.

## Test Credentials
- N/A — storefront routes public.

## ⚠️ PERMANENT SHOPIFY TOKEN FIX (2026-06-28) — IMPORTANT
- Root cause of recurring "Curating the collection…" / 502: the Shopify dev-dashboard app's Admin token EXPIRES ~24h. Any static SHOPIFY_ADMIN_TOKEN dies daily (401).
- Fix: backend auto-fetches & caches a fresh token via client_credentials grant (POST https://{store}/admin/oauth/access_token) using SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET, refreshing 5 min before expiry. See server.py fetch_shopify_token_via_client_credentials() / resolve_shopify_token().
- backend/.env now has: SHOPIFY_STORE_DOMAIN, SHOPIFY_CLIENT_ID, SHOPIFY_CLIENT_SECRET (SHOPIFY_ADMIN_TOKEN kept only as fallback).
- ACTION FOR USER: add SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET to Railway env vars and redeploy so production/custom-domain stays online automatically.
- Verified iteration_12.json (100%). Regression test: backend/tests/test_shopify_token_autorefresh.py. Live variant sample: 43466208018521 (slug bridal-spark-ring-rings).

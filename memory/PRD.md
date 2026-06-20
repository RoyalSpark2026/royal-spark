# PRD — Royal Spark

Date: 2026-06-14

## Original Problem Statement
can a build Jwellary Store and connect to Shopify for Jewllary Store ?

## User Choices
- Full storefront with cart, wishlist, categories, search, and reviews
- Luxury and elegant brand direction
- Mixed jewelry catalog plus custom/made-to-order jewelry
- Build the store first; connect Shopify later when credentials/store are available

## Architecture Decisions
- Frontend: React with routed pages for Home, Shop, Product Detail, and Bespoke Inquiry
- Backend: FastAPI with catalog, product detail, bespoke inquiry, and Shopify-readiness endpoints
- Database: MongoDB used for bespoke inquiry submissions
- Store state: local browser persistence for cart and wishlist
- Shopify strategy: storefront structured for later Shopify mapping of products, collections, inventory, and checkout redirects

## User Personas
- Style-conscious shoppers browsing fine jewelry collections
- Bridal and milestone buyers comparing premium pieces
- Custom jewelry clients seeking bespoke commissions
- Store owner preparing to connect a future Shopify catalog

## Core Requirements
- Elegant luxury storefront experience
- Product discovery via categories and search
- Product detail pages with reviews and material choices
- Cart and wishlist flow
- Bespoke/custom jewelry inquiry submission
- Future-ready Shopify connection path

## What's Been Implemented
### 2026-06-14
- Built Maison Aurelle luxury storefront UI with editorial homepage, hero section, collections, atelier story, and testimonials
- Added Shop page with category filters, search, and customizable-only filtering
- Added Product Detail page with image gallery, material selection, reviews, and add-to-cart / wishlist actions
- Added slide-out cart with quantity controls and removal
- Added Bespoke Inquiry page connected to backend submission API
- Added FastAPI catalog APIs, product detail API, bespoke inquiry API, and Shopify readiness API
- Stored bespoke inquiries in MongoDB
- Added responsive navigation, mobile menu, and complete data-testid coverage for key UI flows
- Updated storefront branding to Royal Spark, with phone in the header and full contact details in the footer
- Re-themed the storefront with a blue-and-gold campaign style, loaded uploaded PNG campaign visuals, and refreshed the seeded catalog toward rings, grillz, chains, and bracelets
- Added requested category structure: Chains, Bangles, Grillz, Charms, Rings, Earrings, Bracelets, Moissanite filter, and Contact page/section
- Removed all existing sample products and replaced homepage/category product areas with luxury Coming Soon states to prepare for live Shopify catalog connection
- Added homepage brand-film section using the uploaded video, updated copy/tagline toward the video mood, and removed landing-page images in favor of elegant placeholders for final assets
- Replaced the split homepage hero with one full-width top video hero using the uploaded brand film, including on-page controls and cinematic copy

## Prioritized Backlog
### P0
- Connect real Shopify store credentials and replace local catalog with Shopify product/collection sync
- Add Shopify checkout redirect / buy flow

### P1
- Add product sorting controls and richer review management
- Add image/file upload support for bespoke inspiration submissions
- Add admin-friendly CMS or product editing workflow

### P2
- Add customer accounts, order history, and saved bespoke consultations
- Add editorial campaign pages and gifting/occasion landing pages
- Add analytics-driven featured collection management

## Next Tasks
- Connect Shopify once store credentials are available
- Map local product schema to Shopify products, collections, and inventory fields
- Add checkout redirection and live product sync status in the UI
- Expand bespoke intake with attachments and consultation scheduling

- Extracted a cleaner logo crop from the latest uploaded artwork and replaced the site logo usage across the shared header/footer layout

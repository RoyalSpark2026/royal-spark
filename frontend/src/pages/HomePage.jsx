import { ArrowRight, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import { Link, useOutletContext } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { ProductCard } from "@/components/ProductCard";
import { fetchHomeData, fetchShopifyReadiness } from "@/lib/api";

export default function HomePage() {
  const storefront = useOutletContext();
  const { data: homeData, isLoading } = useQuery({ queryKey: ["home-data"], queryFn: fetchHomeData });
  const { data: shopifyReadiness } = useQuery({ queryKey: ["shopify-readiness"], queryFn: fetchShopifyReadiness });

  if (isLoading || !homeData) {
    return <div className="px-6 py-24 text-center text-sm text-[#666666]" data-testid="home-loading-state">Curating the collection…</div>;
  }

  return (
    <div data-testid="home-page">
      <section className="mx-auto grid max-w-7xl gap-8 px-6 py-8 md:px-10 lg:grid-cols-[1.05fr_0.95fr] lg:px-16 lg:py-12">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="relative overflow-hidden rounded-[38px] border border-white/10 bg-[linear-gradient(145deg,_rgba(13,24,53,0.98),_rgba(10,18,38,0.92))] p-8 text-[#fdfbf7] md:p-12"
          data-testid="home-hero-content"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(77,124,255,0.28),_transparent_32%),radial-gradient(circle_at_bottom_right,_rgba(216,184,93,0.2),_transparent_24%)]" />
          <div className="relative z-10 max-w-xl">
            <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="hero-eyebrow">Blue label jewelry campaign</p>
            <h1 className="mt-6 font-display text-5xl leading-[0.95] md:text-6xl" data-testid="hero-heading">
              Rings and grillz with a high-shine luxury edge.
            </h1>
            <p className="mt-6 max-w-lg text-sm leading-relaxed text-white/75 md:text-base" data-testid="hero-description">
              Royal Spark now presents a polished luxury storefront while the live Shopify catalog is being prepared for launch.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Button asChild className="h-12 rounded-full bg-[#d8b85d] px-6 text-[#081226] hover:bg-[#f0d78d]" data-testid="hero-shop-button">
                <Link to="/shop">Browse categories <ArrowRight className="h-4 w-4" /></Link>
              </Button>
              <Button asChild variant="outline" className="h-12 rounded-full border-[#d8b85d]/40 bg-transparent text-white hover:bg-white/10" data-testid="hero-bespoke-button">
                <Link to="/bespoke">Start bespoke request</Link>
              </Button>
            </div>
            <div className="mt-10 flex flex-wrap gap-3 text-xs uppercase tracking-[0.24em] text-[#d9e0ff]">
              <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2" data-testid="hero-feature-rings">Shopify-ready catalog</span>
              <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2" data-testid="hero-feature-grills">Curated categories</span>
              <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2" data-testid="hero-feature-chains">Luxury launch in progress</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7, delay: 0.15 }}
          className="grid gap-4"
          data-testid="home-hero-visual"
        >
          <div className="rounded-[38px] border border-white/10 bg-[radial-gradient(circle_at_top,_rgba(216,184,93,0.18),_transparent_28%),linear-gradient(180deg,_rgba(18,31,63,1),_rgba(8,18,38,0.98))] p-8 backdrop-blur" data-testid="hero-image-card">
            <div className="aspect-[4/5] rounded-[30px] border border-white/10 bg-[linear-gradient(160deg,_rgba(255,255,255,0.03),_rgba(255,255,255,0.01))] p-8">
              <div className="flex h-full flex-col justify-between rounded-[24px] border border-dashed border-[#d8b85d]/25 bg-[#0c1733]/50 p-6" data-testid="hero-image-placeholder">
                <div>
                  <p className="text-xs uppercase tracking-[0.28em] text-[#d8b85d]" data-testid="hero-placeholder-eyebrow">Landing visual needed</p>
                  <h2 className="mt-4 font-display text-4xl leading-none text-white" data-testid="hero-product-name">Model wearing jewelry</h2>
                </div>
                <p className="max-w-sm text-sm leading-relaxed text-[#cbd2ec]" data-testid="hero-product-price">
                  Upload a luxury portrait hero image here later. Recommended size: 1920 × 1080 or 1600 × 900.
                </p>
              </div>
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="aspect-[4/3] rounded-[28px] border border-white/10 bg-[linear-gradient(145deg,_rgba(16,32,67,1),_rgba(9,17,36,0.98))] p-6" data-testid="hero-promo-image-one">
              <div className="flex h-full flex-col justify-between rounded-[22px] border border-dashed border-[#d8b85d]/20 bg-white/5 p-5">
                <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]">Future banner 01</p>
                <p className="font-display text-3xl text-white">Product collage / banner</p>
                <p className="text-sm text-[#cbd2ec]">Best size: 1920 × 1080</p>
              </div>
            </div>
            <div className="aspect-[4/3] rounded-[28px] border border-white/10 bg-[linear-gradient(145deg,_rgba(16,32,67,1),_rgba(9,17,36,0.98))] p-6" data-testid="hero-promo-image-two">
              <div className="flex h-full flex-col justify-between rounded-[22px] border border-dashed border-[#d8b85d]/20 bg-white/5 p-5">
                <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]">Future banner 02</p>
                <p className="font-display text-3xl text-white">Logo-focused luxury banner</p>
                <p className="text-sm text-[#cbd2ec]">Best size: 1920 × 1080</p>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-20 md:px-10 lg:px-16" data-testid="featured-collections-section">
        <div className="mb-10 flex items-end justify-between gap-4">
          <div>
          <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="collections-eyebrow">Curated pathways</p>
          <h2 className="mt-3 font-display text-4xl text-white" data-testid="collections-heading">Collections shaped for sparkle-first selling</h2>
          </div>
          <Link to="/shop" className="text-sm uppercase tracking-[0.24em] text-[#d8b85d]" data-testid="collections-view-all-link">View all</Link>
        </div>

        <div className="mb-8 flex flex-wrap gap-3" data-testid="homepage-category-chip-row">
          {["Chains", "Bangles", "Grillz", "Charms", "Rings", "Earrings", "Bracelets", "Moissanite", "Contact"].map((item) => (
            <span
              key={item}
              className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.24em] text-[#d9e0ff]"
              data-testid={`homepage-category-chip-${item.toLowerCase()}`}
            >
              {item}
            </span>
          ))}
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr_0.8fr]">
          {homeData.collections.map((collection, index) => (
            <motion.div
              key={collection.id}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.5, delay: index * 0.08 }}
              className="group overflow-hidden rounded-[34px] border border-white/10 bg-[#111d3a]"
              data-testid={`collection-card-${collection.id}`}
            >
              <div className="aspect-[4/3] border-b border-white/10 bg-[linear-gradient(160deg,_rgba(16,32,67,1),_rgba(9,17,36,0.98))] p-6" data-testid={`collection-image-${collection.id}`}>
                <div className="flex h-full flex-col justify-between rounded-[24px] border border-dashed border-[#d8b85d]/20 bg-white/5 p-5">
                  <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]">Category image needed</p>
                  <p className="font-display text-3xl text-white">{collection.name}</p>
                  <p className="text-sm text-[#cbd2ec]">Best size: 1200 × 1500</p>
                </div>
              </div>
              <div className="space-y-3 p-6">
                <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]" data-testid={`collection-category-${collection.id}`}>{collection.category}</p>
                <h3 className="font-display text-3xl text-white" data-testid={`collection-name-${collection.id}`}>{collection.name}</h3>
                <p className="text-sm text-[#cbd2ec]" data-testid={`collection-description-${collection.id}`}>{collection.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="bg-[linear-gradient(180deg,_rgba(7,17,38,0.9),_rgba(12,27,57,0.95))] py-20 text-[#fdfbf7]" data-testid="atelier-section">
        <div className="mx-auto grid max-w-7xl gap-10 px-6 md:px-10 lg:grid-cols-[0.9fr_1.1fr] lg:px-16">
          <div className="aspect-[4/5] rounded-[34px] border border-white/10 bg-[linear-gradient(160deg,_rgba(16,32,67,1),_rgba(9,17,36,0.98))] p-6" data-testid="atelier-image">
            <div className="flex h-full flex-col justify-between rounded-[28px] border border-dashed border-[#d8b85d]/20 bg-white/5 p-6">
              <p className="text-xs uppercase tracking-[0.28em] text-[#d8b85d]">Brand / story image needed</p>
              <p className="font-display text-4xl text-white">Luxury showroom or close-up craftsmanship</p>
              <p className="text-sm text-[#cbd2ec]">Best size: 1200 × 1500 or 1600 × 2000</p>
            </div>
          </div>
          <div className="self-center">
            <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="atelier-eyebrow">Royal Spark campaign</p>
            <h2 className="mt-4 font-display text-4xl md:text-5xl" data-testid="atelier-heading">{homeData.atelier_story.title}</h2>
            <p className="mt-6 max-w-xl text-sm leading-relaxed text-white/72 md:text-base" data-testid="atelier-description">{homeData.atelier_story.description}</p>
            <div className="mt-8 inline-flex items-center gap-3 rounded-full border border-white/15 bg-white/5 px-5 py-3 text-sm" data-testid="atelier-pill">
              <Sparkles className="h-4 w-4 text-[#d8b85d]" /> Built for retail campaigns, social selling, and premium presentation.
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-20 md:px-10 lg:px-16" data-testid="campaign-gallery-section">
        <div className="mb-10 max-w-2xl">
          <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="campaign-gallery-eyebrow">Uploaded campaign visuals</p>
          <h2 className="mt-4 font-display text-4xl text-white" data-testid="campaign-gallery-heading">Future landing banners are ready for replacement</h2>
        </div>
        <div className="grid gap-6 lg:grid-cols-3">
          {["Hero model wearing jewelry", "Product collage / collection banner", "Logo-focused campaign graphic"].map((label, index) => (
            <div key={label} className="overflow-hidden rounded-[34px] border border-white/10 bg-[#111d3a] p-3" data-testid={`campaign-panel-${index}`}>
              <div className="aspect-[4/5] rounded-[26px] bg-[linear-gradient(160deg,_rgba(16,32,67,1),_rgba(9,17,36,0.98))] p-6" data-testid={`campaign-panel-image-${index}`}>
                <div className="flex h-full flex-col justify-between rounded-[22px] border border-dashed border-[#d8b85d]/20 bg-white/5 p-5">
                  <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]">Landing image needed</p>
                  <p className="font-display text-3xl text-white">{label}</p>
                  <p className="text-sm text-[#cbd2ec]">Best size: 1920 × 1080</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-20 md:px-10 lg:px-16" data-testid="featured-products-section">
        <div className="mb-10 max-w-2xl">
          <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="featured-products-eyebrow">Most loved pieces</p>
          <h2 className="mt-4 font-display text-4xl text-white" data-testid="featured-products-heading">Selected for fast client approval</h2>
        </div>
        {homeData.featured_products.length === 0 ? (
          <div className="rounded-[34px] border border-[#d8b85d]/20 bg-[#111d3a] px-8 py-16 text-center" data-testid="homepage-coming-soon-products">
            <p className="text-xs uppercase tracking-[0.28em] text-[#d8b85d]" data-testid="homepage-coming-soon-eyebrow">Coming soon</p>
            <h3 className="mt-4 font-display text-4xl text-white" data-testid="homepage-coming-soon-heading">Product collections are being prepared.</h3>
            <p className="mx-auto mt-4 max-w-2xl text-sm leading-relaxed text-[#cbd2ec]" data-testid="homepage-coming-soon-description">
              We’re replacing sample items with the client’s real Shopify catalog. The launch collection will appear here once product images, pricing, and categories are finalized.
            </p>
          </div>
        ) : (
          <div className="grid gap-6 lg:grid-cols-3">
            {homeData.featured_products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                isWishlisted={storefront.wishlistIds.includes(product.id)}
                onToggleWishlist={storefront.toggleWishlist}
                onAddToCart={storefront.addToCart}
              />
            ))}
          </div>
        )}
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-24 md:px-10 lg:px-16" data-testid="testimonials-section">
        <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
          <div className="rounded-[34px] border border-white/10 bg-[#111d3a]/90 p-8" data-testid="shopify-readiness-card">
            <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]">Future Shopify connection</p>
            <h3 className="mt-4 font-display text-3xl text-white" data-testid="shopify-readiness-heading">Built to connect later</h3>
            <p className="mt-4 text-sm leading-relaxed text-[#cbd2ec]" data-testid="shopify-readiness-next-step">{shopifyReadiness?.next_step}</p>
            <div className="mt-6 flex flex-wrap gap-2">
              {shopifyReadiness?.supported_sync_targets?.map((target) => (
                <span key={target} className="rounded-full border border-[#d8b85d]/30 bg-[#d8b85d]/10 px-3 py-1 text-xs uppercase tracking-[0.16em] text-[#d8b85d]" data-testid={`shopify-support-${target.replace(/\s+/g, "-")}`}>
                  {target}
                </span>
              ))}
            </div>
          </div>

          <div className="grid gap-5 sm:grid-cols-2">
            {homeData.testimonials.map((review, index) => (
              <motion.div
                key={`${review.author}-${index}`}
                initial={{ opacity: 0, y: 18 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.45, delay: index * 0.08 }}
                className="rounded-[34px] border border-white/10 bg-[#111d3a] p-7"
                data-testid={`testimonial-card-${index}`}
              >
                <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]" data-testid={`testimonial-author-${index}`}>{review.author}</p>
                <h3 className="mt-3 font-display text-3xl leading-none text-white" data-testid={`testimonial-title-${index}`}>{review.title}</h3>
                <p className="mt-4 text-sm leading-relaxed text-[#cbd2ec]" data-testid={`testimonial-comment-${index}`}>{review.comment}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

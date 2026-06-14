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
      <section className="mx-auto grid max-w-7xl gap-8 px-6 py-8 md:px-10 lg:grid-cols-[1.1fr_0.9fr] lg:px-16 lg:py-12">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="relative overflow-hidden rounded-[38px] bg-[#0a0a0a] p-8 text-[#fdfbf7] md:p-12"
          data-testid="home-hero-content"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(197,160,89,0.4),_transparent_38%)]" />
          <div className="relative z-10 max-w-xl">
            <p className="text-xs uppercase tracking-[0.32em] text-[#cab995]" data-testid="hero-eyebrow">Luxury jewelry storefront</p>
            <h1 className="mt-6 font-display text-5xl leading-[0.95] md:text-6xl" data-testid="hero-heading">
              Quiet brilliance for milestone moments.
            </h1>
            <p className="mt-6 max-w-lg text-sm leading-relaxed text-white/75 md:text-base" data-testid="hero-description">
              Discover rings, necklaces, bracelets, earrings, and custom pieces arranged with editorial clarity and atelier-level trust.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Button asChild className="h-12 rounded-full bg-[#c5a059] px-6 text-[#0a0a0a] hover:bg-[#dcc089]" data-testid="hero-shop-button">
                <Link to="/shop">Shop collection <ArrowRight className="h-4 w-4" /></Link>
              </Button>
              <Button asChild variant="outline" className="h-12 rounded-full border-white/40 bg-transparent text-white hover:bg-white/10" data-testid="hero-bespoke-button">
                <Link to="/bespoke">Start bespoke request</Link>
              </Button>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7, delay: 0.15 }}
          className="overflow-hidden rounded-[38px] border border-white/60 bg-white/75 p-3 backdrop-blur"
          data-testid="home-hero-visual"
        >
          <img
            src={homeData.hero_product.hero_image}
            alt={homeData.hero_product.name}
            className="aspect-[4/5] w-full rounded-[30px] object-cover"
            data-testid="hero-image"
          />
          <div className="grid gap-3 px-3 py-5 sm:grid-cols-[1fr_auto] sm:items-end">
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-[#7d5f2d]" data-testid="hero-product-category">Featured ring</p>
              <h2 className="mt-2 font-display text-4xl leading-none text-[#0a0a0a]" data-testid="hero-product-name">{homeData.hero_product.name}</h2>
            </div>
            <p className="text-sm text-[#022b22]" data-testid="hero-product-price">{homeData.hero_product.formatted_price}</p>
          </div>
        </motion.div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-20 md:px-10 lg:px-16" data-testid="featured-collections-section">
        <div className="mb-10 flex items-end justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.32em] text-[#7d5f2d]" data-testid="collections-eyebrow">Curated pathways</p>
            <h2 className="mt-3 font-display text-4xl text-[#0a0a0a]" data-testid="collections-heading">Collections shaped by occasion</h2>
          </div>
          <Link to="/shop" className="text-sm uppercase tracking-[0.24em] text-[#022b22]" data-testid="collections-view-all-link">View all</Link>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr_0.8fr]">
          {homeData.collections.map((collection, index) => (
            <motion.div
              key={collection.id}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.5, delay: index * 0.08 }}
              className="group overflow-hidden rounded-[34px] border border-[#ece4d8] bg-white"
              data-testid={`collection-card-${collection.id}`}
            >
              <img src={collection.image} alt={collection.name} className="aspect-[4/3] w-full object-cover transition duration-700 group-hover:scale-105" data-testid={`collection-image-${collection.id}`} />
              <div className="space-y-3 p-6">
                <p className="text-xs uppercase tracking-[0.24em] text-[#7d5f2d]" data-testid={`collection-category-${collection.id}`}>{collection.category}</p>
                <h3 className="font-display text-3xl text-[#0a0a0a]" data-testid={`collection-name-${collection.id}`}>{collection.name}</h3>
                <p className="text-sm text-[#5f5a52]" data-testid={`collection-description-${collection.id}`}>{collection.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="bg-[#0a0a0a] py-20 text-[#fdfbf7]" data-testid="atelier-section">
        <div className="mx-auto grid max-w-7xl gap-10 px-6 md:px-10 lg:grid-cols-[0.9fr_1.1fr] lg:px-16">
          <img src={homeData.atelier_story.image} alt="Jewelry craftsmanship" className="aspect-[4/5] w-full rounded-[34px] object-cover" data-testid="atelier-image" />
          <div className="self-center">
            <p className="text-xs uppercase tracking-[0.32em] text-[#c5a059]" data-testid="atelier-eyebrow">The atelier</p>
            <h2 className="mt-4 font-display text-4xl md:text-5xl" data-testid="atelier-heading">{homeData.atelier_story.title}</h2>
            <p className="mt-6 max-w-xl text-sm leading-relaxed text-white/72 md:text-base" data-testid="atelier-description">{homeData.atelier_story.description}</p>
            <div className="mt-8 inline-flex items-center gap-3 rounded-full border border-white/15 bg-white/5 px-5 py-3 text-sm" data-testid="atelier-pill">
              <Sparkles className="h-4 w-4 text-[#c5a059]" /> Handmade with measured restraint and lasting materials.
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-20 md:px-10 lg:px-16" data-testid="featured-products-section">
        <div className="mb-10 max-w-2xl">
          <p className="text-xs uppercase tracking-[0.32em] text-[#7d5f2d]" data-testid="featured-products-eyebrow">Most loved pieces</p>
          <h2 className="mt-4 font-display text-4xl text-[#0a0a0a]" data-testid="featured-products-heading">Selected for graceful first impressions</h2>
        </div>
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
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-24 md:px-10 lg:px-16" data-testid="testimonials-section">
        <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
          <div className="rounded-[34px] border border-[#e7e1d7] bg-white/70 p-8" data-testid="shopify-readiness-card">
            <p className="text-xs uppercase tracking-[0.32em] text-[#7d5f2d]">Future Shopify connection</p>
            <h3 className="mt-4 font-display text-3xl text-[#0a0a0a]" data-testid="shopify-readiness-heading">Built to connect later</h3>
            <p className="mt-4 text-sm leading-relaxed text-[#5f5a52]" data-testid="shopify-readiness-next-step">{shopifyReadiness?.next_step}</p>
            <div className="mt-6 flex flex-wrap gap-2">
              {shopifyReadiness?.supported_sync_targets?.map((target) => (
                <span key={target} className="rounded-full border border-[#d8ccb8] bg-[#fbf7f1] px-3 py-1 text-xs uppercase tracking-[0.16em] text-[#022b22]" data-testid={`shopify-support-${target.replace(/\s+/g, "-")}`}>
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
                className="rounded-[34px] border border-[#ece4d8] bg-white p-7"
                data-testid={`testimonial-card-${index}`}
              >
                <p className="text-xs uppercase tracking-[0.24em] text-[#7d5f2d]" data-testid={`testimonial-author-${index}`}>{review.author}</p>
                <h3 className="mt-3 font-display text-3xl leading-none text-[#0a0a0a]" data-testid={`testimonial-title-${index}`}>{review.title}</h3>
                <p className="mt-4 text-sm leading-relaxed text-[#5f5a52]" data-testid={`testimonial-comment-${index}`}>{review.comment}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

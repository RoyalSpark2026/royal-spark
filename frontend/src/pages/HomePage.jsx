import { ArrowRight, Volume2 } from "lucide-react";
import { motion } from "framer-motion";
import { Link, useOutletContext } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useRef, useState } from "react";

import { Button } from "@/components/ui/button";
import { ProductCard } from "@/components/ProductCard";
import { fetchHomeData } from "@/lib/api";

const heroFilmUrl = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/yj0dyksy_generated_video%20%281%29.mp4";
const signatureCategoryImages = [
  {
    title: "Rings",
    copy: "Statement silhouettes with refined brilliance and a strong ceremonial feel.",
    image: "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/zunjm4jc_426b8562-73d0-4980-b0fa-67c1b86f59ff.jpg",
  },
  {
    title: "Grillz",
    copy: "Bold custom expression shaped with polished metal finishes and standout shine.",
    image: "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/2ho4vbhh_92778eea-ecad-464d-b41f-0d1ec4466d99.jpg",
  },
  {
    title: "Chains",
    copy: "Layering pieces and strong links designed to complete a premium jewelry wardrobe.",
    image: "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/6wsdgjdk_de550993-6d1f-44b3-a299-5e507be1f0e6.jpg",
  },
];

export default function HomePage() {
  const storefront = useOutletContext();
  const { data: homeData, isLoading } = useQuery({ queryKey: ["home-data"], queryFn: fetchHomeData });
  const [heroMuted, setHeroMuted] = useState(true);
  const heroVideoRef = useRef(null);

  useEffect(() => {
    const videoElement = heroVideoRef.current;
    if (!videoElement) return;

    videoElement.muted = heroMuted;
    if (!heroMuted) {
      videoElement.play().catch(() => {
        setHeroMuted(true);
      });
    }
  }, [heroMuted]);

  useEffect(() => {
    const videoElement = heroVideoRef.current;
    const heroWrapper = document.querySelector('[data-testid="home-hero-video-wrapper"]');
    if (!videoElement || !heroWrapper) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          videoElement.play().catch(() => {});
        } else {
          videoElement.pause();
        }
      },
      { threshold: 0.35 },
    );

    observer.observe(heroWrapper);
    return () => observer.disconnect();
  }, []);

  if (isLoading || !homeData) {
    return <div className="px-6 py-24 text-center text-sm text-[#666666]" data-testid="home-loading-state">Curating the collection…</div>;
  }

  return (
    <div data-testid="home-page">
      <section className="mx-auto max-w-7xl px-6 py-8 md:px-10 lg:px-16 lg:py-12" data-testid="home-hero-section">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="relative overflow-hidden rounded-[38px] border border-white/10 bg-[#050b18]"
          data-testid="home-hero-video-wrapper"
        >
          <div className="relative aspect-[16/10] w-full overflow-hidden bg-black">
            <video
              ref={heroVideoRef}
              src={heroFilmUrl}
              className="h-full w-full object-cover"
              autoPlay
              controls
              loop
              playsInline
              muted={heroMuted}
              preload="auto"
              data-testid="hero-full-video"
            />
            <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(6,12,28,0.06),rgba(6,12,28,0.2))]" />
            <div className="absolute inset-x-0 top-0 flex justify-end p-5 md:p-6">
              <button
                type="button"
                onClick={() => setHeroMuted((current) => !current)}
                className="inline-flex items-center gap-2 rounded-full border border-[#d8b85d]/40 bg-[#081226]/70 px-4 py-2 text-xs uppercase tracking-[0.22em] text-[#f4d98e] backdrop-blur"
                data-testid="hero-video-sound-toggle"
              >
                <Volume2 className="h-4 w-4" /> {heroMuted ? "Enable sound" : "Mute sound"}
              </button>
            </div>
            <div className="absolute left-0 right-0 top-0 px-5 py-5 md:px-8 md:py-8">
              <div className="max-w-xl rounded-[24px] border border-white/10 bg-[#081226]/46 p-4 backdrop-blur-md md:p-5">
                <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="hero-eyebrow">Discover exquisite elegance</p>
                <h1 className="mt-2 font-display text-3xl leading-[0.98] text-white md:text-4xl" data-testid="hero-heading">
                  Where luxury meets craftsmanship.
                </h1>
                <p className="mt-3 max-w-lg text-sm leading-relaxed text-white/76" data-testid="hero-description">
                  Royal Spark presents regal detail, refined craftsmanship, and bold jewelry with a polished luxury presence.
                </p>
                <div className="mt-5 flex flex-wrap gap-3">
                  <Button asChild className="h-10 rounded-full bg-[#d8b85d] px-4 text-[#081226] hover:bg-[#f0d78d]" data-testid="hero-shop-button">
                    <Link to="/shop">Browse categories <ArrowRight className="h-4 w-4" /></Link>
                  </Button>
                  <Button asChild variant="outline" className="h-10 rounded-full border-[#d8b85d]/40 bg-transparent text-white hover:bg-white/10" data-testid="hero-bespoke-button">
                    <Link to="/bespoke">Start bespoke request</Link>
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-6 md:px-10 lg:px-16" data-testid="feature-grid-section">
        <div className="mb-10 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="feature-grid-eyebrow">Signature categories</p>
            <h2 className="mt-4 font-display text-5xl leading-none text-white" data-testid="feature-grid-heading">Three signature directions for the collection.</h2>
          </div>
          <p className="max-w-xl text-sm leading-relaxed text-[#cbd2ec]" data-testid="feature-grid-description">
            A refined edit of the categories that define the Royal Spark identity.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3" data-testid="feature-grid-cards">
          {signatureCategoryImages.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.45, delay: index * 0.08 }}
              className="overflow-hidden rounded-[32px] border border-white/10 bg-[linear-gradient(160deg,_rgba(14,28,58,1),_rgba(7,16,36,0.98))]"
              data-testid={`feature-grid-card-${index}`}
            >
              <Link
                to={`/shop?category=${feature.title === "Grillz" ? "Grills" : feature.title}`}
                className="block h-full transition hover:bg-white/5"
                data-testid={`feature-grid-card-link-${index}`}
              >
                <div className="aspect-[4/5] overflow-hidden border-b border-white/10 bg-[#071126]" data-testid={`feature-grid-card-image-wrapper-${index}`}>
                  <img
                    src={feature.image}
                    alt={feature.title}
                    className="h-full w-full object-cover transition duration-700 hover:scale-105"
                    data-testid={`feature-grid-card-image-${index}`}
                  />
                </div>
                <div className="p-7">
                  <p className="text-xs uppercase tracking-[0.28em] text-[#d8b85d]" data-testid={`feature-grid-card-eyebrow-${index}`}>Feature {index + 1}</p>
                  <h3 className="mt-5 font-display text-4xl text-white" data-testid={`feature-grid-card-title-${index}`}>{feature.title}</h3>
                  <p className="mt-4 text-sm leading-relaxed text-[#cbd2ec]" data-testid={`feature-grid-card-copy-${index}`}>{feature.copy}</p>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </section>

      {homeData.featured_products?.length ? (
        <section className="mx-auto max-w-7xl px-6 pb-20 pt-8 md:px-10 lg:px-16" data-testid="homepage-live-products-section">
          <div className="mb-10 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="homepage-live-products-eyebrow">Latest arrivals</p>
              <h2 className="mt-4 font-display text-5xl leading-none text-white" data-testid="homepage-live-products-heading">Live pieces from the Royal Spark collection.</h2>
            </div>
            <Link to="/shop" className="text-sm uppercase tracking-[0.24em] text-[#d8b85d]" data-testid="homepage-live-products-link">View all products</Link>
          </div>

          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3" data-testid="homepage-live-products-grid">
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
      ) : null}

    </div>
  );
}
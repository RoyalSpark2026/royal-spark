import { useOutletContext, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { ProductCard } from "@/components/ProductCard";
import { fetchProducts } from "@/lib/api";

export default function ShopPage() {
  const storefront = useOutletContext();
  const [searchParams, setSearchParams] = useSearchParams();
  const activeCategory = searchParams.get("category") || "All";
  const moissaniteOnly = searchParams.get("material") === "Moissanite";
  const pageTitle = moissaniteOnly ? "Moissanite Selection" : activeCategory === "All" ? "All Collections" : activeCategory;
  const pageDescription = moissaniteOnly
    ? "Cleanly curated moissanite pieces with strong brilliance and modern luxury styling."
    : `Browse ${activeCategory === "All" ? "every available category" : activeCategory.toLowerCase()} with a clean catalog-first view.`;

  const { data, isLoading } = useQuery({
    queryKey: ["products", activeCategory, moissaniteOnly],
    queryFn: () => fetchProducts({
      category: activeCategory,
      material: moissaniteOnly ? "Moissanite" : undefined,
    }),
  });

  return (
    <div className="mx-auto max-w-7xl px-6 py-10 md:px-10 lg:px-16" data-testid="shop-page">
      <section data-testid="shop-results-section">
        <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]" data-testid="shop-results-eyebrow">Available now</p>
            <h1 className="mt-3 font-display text-4xl text-white" data-testid="shop-heading">{pageTitle}</h1>
            <p className="mt-3 max-w-2xl text-sm text-[#cbd2ec]" data-testid="shop-heading-description">{pageDescription}</p>
          </div>
          <div className="flex items-center gap-3">
            {moissaniteOnly ? (
              <button
                type="button"
                onClick={() => setSearchParams(activeCategory === "All" ? {} : { category: activeCategory })}
                className="rounded-full border border-[#d8b85d]/30 bg-[#d8b85d]/10 px-4 py-2 text-xs uppercase tracking-[0.24em] text-[#d8b85d]"
                data-testid="shop-clear-moissanite-filter-button"
              >
                Clear Moissanite filter
              </button>
            ) : null}
            <p className="text-sm text-[#cbd2ec]" data-testid="shop-results-count">
              {isLoading && !data ? "Curating pieces…" : `${data?.total ?? 0} pieces found`}
            </p>
          </div>
        </div>

        {isLoading ? (
          <div className="rounded-[34px] border border-white/10 bg-[#111d3a] p-10 text-center text-sm text-[#cbd2ec]" data-testid="shop-loading-state">
            Arranging the showcase…
          </div>
        ) : data?.items?.length === 0 ? (
          <div className="rounded-[34px] border border-[#d8b85d]/20 bg-[#111d3a] px-8 py-16 text-center" data-testid="shop-empty-state">
            <p className="text-xs uppercase tracking-[0.28em] text-[#d8b85d]" data-testid="shop-empty-state-eyebrow">Coming soon</p>
            <h2 className="mt-4 font-display text-4xl text-white" data-testid="shop-empty-state-heading">This collection is being prepared.</h2>
            <p className="mx-auto mt-4 max-w-2xl text-sm leading-relaxed text-[#cbd2ec]" data-testid="shop-empty-state-description">
              Royal Spark is curating this category with the same premium standard. Check back soon for new arrivals and featured pieces.
            </p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3" data-testid="shop-product-grid">
            {data?.items.map((product) => (
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
    </div>
  );
}

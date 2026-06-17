import { Search } from "lucide-react";
import { useMemo, useState } from "react";
import { useNavigate, useOutletContext, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { ProductCard } from "@/components/ProductCard";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { fetchProducts } from "@/lib/api";

const curatedCategories = [
  { label: "Chains", value: "Chains" },
  { label: "Bangles", value: "Bangles" },
  { label: "Grillz", value: "Grills" },
  { label: "Charms", value: "Charms" },
  { label: "Rings", value: "Rings" },
  { label: "Earrings", value: "Earrings" },
  { label: "Bracelets", value: "Bracelets" },
  { label: "Contact", value: "Contact" },
];

export default function ShopPage() {
  const storefront = useOutletContext();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState("");
  const [customOnly, setCustomOnly] = useState(false);
  const activeCategory = searchParams.get("category") || "All";
  const moissaniteOnly = searchParams.get("material") === "Moissanite";

  const { data, isLoading } = useQuery({
    queryKey: ["products", activeCategory, search, customOnly, moissaniteOnly],
    queryFn: () => fetchProducts({
      category: activeCategory,
      search,
      customizable_only: customOnly,
      material: moissaniteOnly ? "Moissanite" : undefined,
    }),
  });

  const categoryButtons = useMemo(() => [{ label: "All", value: "All" }, ...curatedCategories], []);

  return (
    <div className="mx-auto max-w-7xl px-6 py-10 md:px-10 lg:px-16" data-testid="shop-page">
      <div className="grid gap-8 lg:grid-cols-[0.32fr_0.68fr]">
        <aside className="h-fit rounded-[34px] border border-white/10 bg-[#111d3a]/90 p-6" data-testid="shop-filters-panel">
          <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="shop-filters-eyebrow">Catalog filters</p>
          <h1 className="mt-4 font-display text-4xl text-white" data-testid="shop-heading">Browse the collection</h1>

          <div className="mt-8 space-y-4">
            <label className="text-xs uppercase tracking-[0.24em] text-[#cdd5ef]" htmlFor="shop-search-input">Search</label>
            <div className="relative">
              <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-[#d8b85d]" />
              <Input
                id="shop-search-input"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Rings, grillz, chains…"
                className="h-12 rounded-full border-white/10 bg-white/5 pl-11 text-white"
                data-testid="shop-search-input"
              />
            </div>
          </div>

          <div className="mt-8">
            <p className="text-xs uppercase tracking-[0.24em] text-[#cdd5ef]" data-testid="shop-categories-label">Categories</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {categoryButtons.map((category) => (
                <button
                  key={category.label}
                  type="button"
                  onClick={() => {
                    if (category.value === "Contact") {
                      navigate("/contact");
                      return;
                    }
                    if (category.value === "All") {
                      setSearchParams({});
                    } else {
                      setSearchParams({ category: category.value, ...(moissaniteOnly ? { material: "Moissanite" } : {}) });
                    }
                  }}
                  className={`rounded-full px-4 py-2 text-xs uppercase tracking-[0.24em] transition ${
                    activeCategory === category.value ? "bg-[#d8b85d] text-[#081226]" : "border border-white/10 bg-white/5 text-[#d9e0ff] hover:bg-white/10"
                  }`}
                  data-testid={`shop-category-${category.label.toLowerCase().replace(/\s+/g, "-")}`}
                >
                  {category.label}
                </button>
              ))}
            </div>
          </div>

          <div className="mt-8 flex items-center gap-3 rounded-[24px] border border-white/10 bg-white/5 p-4">
            <Checkbox
              id="custom-only-toggle"
              checked={customOnly}
              onCheckedChange={(checked) => setCustomOnly(Boolean(checked))}
              className="border-[#d8b85d] data-[state=checked]:bg-[#d8b85d] data-[state=checked]:text-[#081226]"
              data-testid="shop-custom-only-checkbox"
            />
            <label htmlFor="custom-only-toggle" className="text-sm text-[#d9e0ff]" data-testid="shop-custom-only-label">
              Show only customizable pieces
            </label>
          </div>

          <div className="mt-4 flex items-center gap-3 rounded-[24px] border border-white/10 bg-white/5 p-4">
            <Checkbox
              id="moissanite-only-toggle"
              checked={moissaniteOnly}
              onCheckedChange={(checked) => {
                const nextValue = Boolean(checked);
                const nextParams = {};
                if (activeCategory !== "All") {
                  nextParams.category = activeCategory;
                }
                if (nextValue) {
                  nextParams.material = "Moissanite";
                }
                setSearchParams(nextParams);
              }}
              className="border-[#d8b85d] data-[state=checked]:bg-[#d8b85d] data-[state=checked]:text-[#081226]"
              data-testid="shop-moissanite-only-checkbox"
            />
            <label htmlFor="moissanite-only-toggle" className="text-sm text-[#d9e0ff]" data-testid="shop-moissanite-only-label">
              Show Moissanite only
            </label>
          </div>
        </aside>

        <section data-testid="shop-results-section">
          <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]" data-testid="shop-results-eyebrow">Available now</p>
              <p className="mt-2 text-sm text-[#cbd2ec]" data-testid="shop-results-count">
                {isLoading && !data ? "Curating pieces…" : `${data?.total ?? 0} pieces found`}
              </p>
            </div>
          </div>

          {isLoading ? (
            <div className="rounded-[34px] border border-white/10 bg-[#111d3a] p-10 text-center text-sm text-[#cbd2ec]" data-testid="shop-loading-state">
              Arranging the showcase…
            </div>
          ) : (
            <div className="grid gap-6 xl:grid-cols-2" data-testid="shop-product-grid">
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
    </div>
  );
}

import { Heart, ShoppingBag, Star } from "lucide-react";
import { useMemo, useState } from "react";
import { useOutletContext, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { fetchProductDetail } from "@/lib/api";

const formatMoney = (value) => `$${value.toLocaleString()}`;

export default function ProductDetailPage() {
  const { slug } = useParams();
  const storefront = useOutletContext();
  const { data: product, isLoading } = useQuery({ queryKey: ["product-detail", slug], queryFn: () => fetchProductDetail(slug) });
  const [selectedImage, setSelectedImage] = useState(0);
  const [selectedMaterial, setSelectedMaterial] = useState("");

  const currentMaterial = useMemo(() => selectedMaterial || product?.materials?.[0] || "Signature", [product, selectedMaterial]);

  if (isLoading || !product) {
    return <div className="px-6 py-24 text-center text-sm text-[#666666]" data-testid="product-loading-state">Preparing the product story…</div>;
  }

  return (
    <div className="mx-auto max-w-7xl px-6 py-10 md:px-10 lg:px-16" data-testid="product-detail-page">
      <div className="grid gap-10 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="grid gap-4 lg:grid-cols-[120px_1fr]" data-testid="product-gallery-section">
          <div className="order-2 flex gap-3 overflow-auto lg:order-1 lg:flex-col">
            {product.gallery.map((image, index) => (
              <button
                key={`${image}-${index}`}
                type="button"
                onClick={() => setSelectedImage(index)}
                className={`overflow-hidden rounded-[24px] border ${selectedImage === index ? "border-[#d8b85d]" : "border-white/10"}`}
                data-testid={`product-thumbnail-${index}`}
              >
                <img src={image} alt={`${product.name} view ${index + 1}`} className="h-28 w-24 object-cover" />
              </button>
            ))}
          </div>
          <div className="order-1 overflow-hidden rounded-[36px] border border-white/10 bg-[#111d3a] p-3 lg:order-2">
            <img src={product.gallery[selectedImage]} alt={product.name} className="aspect-[4/5] w-full rounded-[28px] object-cover" data-testid="product-main-image" />
          </div>
        </div>

        <div className="xl:sticky xl:top-28 xl:h-fit" data-testid="product-detail-content">
          <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="product-category-label">{product.category}</p>
          <h1 className="mt-4 font-display text-5xl leading-none text-white" data-testid="product-detail-name">{product.name}</h1>
          <div className="mt-5 flex flex-wrap items-center gap-4 text-sm">
            <span className="text-[#d8b85d]" data-testid="product-detail-price">{formatMoney(product.price)}</span>
            <span className="inline-flex items-center gap-1 rounded-full bg-white/5 px-3 py-1 text-[#f5f7ff]" data-testid="product-detail-rating">
              <Star className="h-3.5 w-3.5 fill-current" /> {product.rating} · {product.review_count} reviews
            </span>
          </div>
          <p className="mt-6 max-w-xl text-sm leading-relaxed text-[#cbd2ec]" data-testid="product-detail-description">{product.description}</p>

          <div className="mt-8">
            <p className="text-xs uppercase tracking-[0.24em] text-[#cbd2ec]" data-testid="product-materials-label">Choose material</p>
            <div className="mt-4 flex flex-wrap gap-3">
              {product.materials.map((material) => (
                <button
                  key={material}
                  type="button"
                  onClick={() => setSelectedMaterial(material)}
                  className={`rounded-full px-4 py-2 text-xs uppercase tracking-[0.22em] transition ${
                    currentMaterial === material ? "bg-[#d8b85d] text-[#081226]" : "border border-white/10 bg-white/5 text-[#d9e0ff]"
                  }`}
                  data-testid={`product-material-${material.toLowerCase().replace(/\s+/g, "-")}`}
                >
                  {material}
                </button>
              ))}
            </div>
          </div>

          <div className="mt-8 flex flex-wrap gap-3">
            <Button
              type="button"
              onClick={() => storefront.addToCart(product, currentMaterial)}
              className="h-12 rounded-full bg-[#d8b85d] px-6 text-[#081226] hover:bg-[#f0d78d]"
              data-testid="product-detail-add-to-cart"
            >
              <ShoppingBag className="h-4 w-4" /> Add to cart
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => storefront.toggleWishlist(product.id)}
              className="h-12 rounded-full border-[#d8b85d]/40 bg-transparent text-white hover:bg-white/10"
              data-testid="product-detail-wishlist"
            >
              <Heart className={`h-4 w-4 ${storefront.wishlistIds.includes(product.id) ? "fill-[#d8b85d] text-[#d8b85d]" : ""}`} />
              Save to wishlist
            </Button>
          </div>

          <div className="mt-8 flex flex-wrap gap-2">
            {product.highlights.map((highlight) => (
              <span key={highlight} className="rounded-full border border-[#d8b85d]/20 bg-[#d8b85d]/10 px-3 py-2 text-xs uppercase tracking-[0.16em] text-[#d8b85d]" data-testid={`product-highlight-${highlight.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}>
                {highlight}
              </span>
            ))}
          </div>

          <Accordion type="single" collapsible className="mt-10 w-full border-t border-white/10" data-testid="product-detail-accordion">
            <AccordionItem value="shipping">
              <AccordionTrigger data-testid="product-shipping-toggle">Shipping & delivery</AccordionTrigger>
              <AccordionContent data-testid="product-shipping-content">Hand-finished pieces ship in 5–10 business days; bespoke items follow your consultation timeline.</AccordionContent>
            </AccordionItem>
            <AccordionItem value="returns">
              <AccordionTrigger data-testid="product-returns-toggle">Returns & care</AccordionTrigger>
              <AccordionContent data-testid="product-returns-content">Complimentary care guidance is included; unworn standard items may be returned within 14 days.</AccordionContent>
            </AccordionItem>
            <AccordionItem value="reviews">
              <AccordionTrigger data-testid="product-reviews-toggle">Reviews</AccordionTrigger>
              <AccordionContent>
                <div className="space-y-4" data-testid="product-reviews-content">
                  {product.reviews.map((review, index) => (
                    <div key={`${review.author}-${index}`} className="rounded-[24px] border border-white/10 bg-white/5 p-4" data-testid={`product-review-${index}`}>
                      <p className="text-xs uppercase tracking-[0.22em] text-[#d8b85d]">{review.author}</p>
                      <h3 className="mt-2 font-display text-2xl text-white">{review.title}</h3>
                      <p className="mt-2 text-sm text-[#cbd2ec]">{review.comment}</p>
                    </div>
                  ))}
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
    </div>
  );
}

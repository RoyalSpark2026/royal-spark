import { Heart, ShoppingBag, Sparkles, Star } from "lucide-react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const formatMoney = (value) => `$${value.toLocaleString()}`;

export const ProductCard = ({ product, isWishlisted, onToggleWishlist, onAddToCart }) => (
  <motion.div
    initial={{ opacity: 0, y: 24 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, amount: 0.2 }}
    transition={{ duration: 0.55 }}
  >
    <Card className="group overflow-hidden rounded-[32px] border border-[#ece4d8] bg-white/90 shadow-none" data-testid={`product-card-${product.slug}`}>
      <div className="relative overflow-hidden">
        <img
          src={product.hero_image}
          alt={product.name}
          className="aspect-[4/5] w-full object-cover transition duration-700 ease-out group-hover:scale-105"
          data-testid={`product-image-${product.slug}`}
        />
        <button
          type="button"
          onClick={() => onToggleWishlist(product.id)}
          className="absolute right-4 top-4 rounded-full border border-white/70 bg-white/80 p-2 text-[#0a0a0a] backdrop-blur transition hover:scale-105"
          data-testid={`wishlist-toggle-${product.slug}`}
        >
          <Heart className={`h-4 w-4 ${isWishlisted ? "fill-[#7d1024] text-[#7d1024]" : ""}`} />
        </button>
      </div>

      <div className="space-y-4 p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-[#7d5f2d]" data-testid={`product-category-${product.slug}`}>
              {product.category}
            </p>
            <Link to={`/shop/${product.slug}`} className="inline-block">
              <h3 className="mt-2 font-display text-[1.9rem] leading-none text-[#0a0a0a]" data-testid={`product-name-${product.slug}`}>
                {product.name}
              </h3>
            </Link>
          </div>
          <div className="rounded-full bg-[#f6f0e6] px-3 py-1 text-xs text-[#022b22]" data-testid={`product-rating-${product.slug}`}>
            <span className="inline-flex items-center gap-1">
              <Star className="h-3.5 w-3.5 fill-current" />
              {product.rating}
            </span>
          </div>
        </div>

        <p className="text-sm leading-relaxed text-[#5f5a52]" data-testid={`product-description-${product.slug}`}>
          {product.short_description}
        </p>

        <div className="flex flex-wrap items-center gap-2 text-xs uppercase tracking-[0.22em] text-[#666666]">
          <span className="rounded-full border border-[#e7e1d7] px-3 py-1" data-testid={`product-price-${product.slug}`}>
            {formatMoney(product.price)}
          </span>
          {product.is_customizable ? (
            <span className="inline-flex items-center gap-1 rounded-full border border-[#d7ccbc] bg-[#fbf7f1] px-3 py-1 text-[#022b22]" data-testid={`product-customizable-${product.slug}`}>
              <Sparkles className="h-3.5 w-3.5" /> Customizable
            </span>
          ) : null}
        </div>

        <div className="grid gap-3 sm:grid-cols-2">
          <Button
            type="button"
            onClick={() => onAddToCart(product)}
            className="h-11 rounded-full bg-[#022b22] text-white hover:bg-[#0a0a0a]"
            data-testid={`add-to-cart-${product.slug}`}
          >
            <ShoppingBag className="h-4 w-4" /> Add to cart
          </Button>
          <Button asChild variant="outline" className="h-11 rounded-full border-[#cab995] bg-transparent hover:bg-[#f5efe5]" data-testid={`view-product-${product.slug}`}>
            <Link to={`/shop/${product.slug}`}>View detail</Link>
          </Button>
        </div>
      </div>
    </Card>
  </motion.div>
);

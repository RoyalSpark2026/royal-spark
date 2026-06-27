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
    className="md:h-full"
  >
    <Card className="group flex flex-col overflow-hidden rounded-[20px] border border-white/10 bg-[#111d3a]/90 text-white shadow-[0_0_30px_rgba(8,18,38,0.35)] md:h-full md:rounded-[32px]" data-testid={`product-card-${product.slug}`}>
      <Link to={`/shop/${product.slug}`} className="relative block overflow-hidden">
        <img
          src={product.hero_image}
          alt={product.name}
          className="aspect-square w-full bg-[#0a1631] object-cover transition duration-700 ease-out group-hover:scale-105 md:aspect-[4/5] md:p-3 md:object-contain"
          data-testid={`product-image-${product.slug}`}
        />
        <button
          type="button"
          onClick={() => onToggleWishlist(product.id)}
          className="absolute right-3 top-3 rounded-full border border-white/20 bg-[#081226]/70 p-2 text-white backdrop-blur transition hover:scale-105 md:right-4 md:top-4"
          data-testid={`wishlist-toggle-${product.slug}`}
        >
          <Heart className={`h-4 w-4 ${isWishlisted ? "fill-[#d8b85d] text-[#d8b85d]" : ""}`} />
        </button>
      </Link>

      <div className="flex flex-col space-y-2 p-3 md:h-full md:space-y-4 md:p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-[0.65rem] uppercase tracking-[0.2em] text-[#d8b85d] md:text-xs md:tracking-[0.24em]" data-testid={`product-category-${product.slug}`}>
              {product.category}
            </p>
            <Link to={`/shop/${product.slug}`} className="inline-block">
              <h3 className="mt-1 font-display text-lg leading-tight text-[#f4f7ff] md:mt-2 md:text-[1.9rem] md:leading-none" data-testid={`product-name-${product.slug}`}>
                {product.name}
              </h3>
            </Link>
          </div>
          <div className="hidden rounded-full bg-[#1a2a51] px-3 py-1 text-xs text-[#d8b85d] md:block" data-testid={`product-rating-${product.slug}`}>
            <span className="inline-flex items-center gap-1">
              <Star className="h-3.5 w-3.5 fill-current" />
              {product.rating}
            </span>
          </div>
        </div>

        <p className="hidden text-sm leading-relaxed text-[#cbd2ec] md:block" data-testid={`product-description-${product.slug}`}>
          {product.short_description}
        </p>

        <div className="flex flex-wrap items-center gap-2 text-xs uppercase tracking-[0.22em] text-[#aeb7d8]">
          <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[#f1f4ff] md:text-[#aeb7d8]" data-testid={`product-price-${product.slug}`}>
            {formatMoney(product.price)}
          </span>
          {product.is_customizable ? (
            <span className="hidden items-center gap-1 rounded-full border border-[#d8b85d]/30 bg-[#d8b85d]/10 px-3 py-1 text-[#d8b85d] md:inline-flex" data-testid={`product-customizable-${product.slug}`}>
              <Sparkles className="h-3.5 w-3.5" /> Customizable
            </span>
          ) : null}
        </div>

        <div className="mt-auto hidden gap-3 sm:grid-cols-2 md:grid" data-testid={`product-actions-${product.slug}`}>
          <Button
            type="button"
            onClick={() => onAddToCart(product)}
            className="h-11 rounded-full bg-[#d8b85d] text-[#081226] hover:bg-[#f0d78d]"
            data-testid={`add-to-cart-${product.slug}`}
          >
            <ShoppingBag className="h-4 w-4" /> Add to cart
          </Button>
          <Button asChild variant="outline" className="h-11 rounded-full border-[#d8b85d]/40 bg-transparent text-[#f1f4ff] hover:bg-white/10" data-testid={`view-product-${product.slug}`}>
            <Link to={`/shop/${product.slug}`}>View detail</Link>
          </Button>
        </div>

        <Button
          type="button"
          onClick={() => onAddToCart(product)}
          className="mt-1 h-9 rounded-full bg-[#d8b85d] text-xs text-[#081226] hover:bg-[#f0d78d] md:hidden"
          data-testid={`mobile-add-to-cart-${product.slug}`}
        >
          <ShoppingBag className="h-3.5 w-3.5" /> Add
        </Button>
      </div>
    </Card>
  </motion.div>
);

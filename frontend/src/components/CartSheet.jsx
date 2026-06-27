import { useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { createCheckout } from "@/lib/api";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

const formatMoney = (value) => `$${value.toLocaleString()}`;

export const CartSheet = ({
  open,
  onOpenChange,
  cartItems,
  subtotal,
  updateCartQuantity,
  removeFromCart,
}) => {
  const [isRedirecting, setIsRedirecting] = useState(false);

  const handleCheckout = async () => {
    const items = cartItems
      .filter((item) => item.variant_id)
      .map((item) => ({ variant_id: String(item.variant_id), quantity: item.quantity }));

    if (items.length === 0) {
      toast.error("Please remove and re-add your items, then checkout again.");
      return;
    }

    try {
      setIsRedirecting(true);
      const { checkout_url } = await createCheckout(items);
      window.location.href = checkout_url;
    } catch (error) {
      setIsRedirecting(false);
      toast.error("We couldn't start checkout. Please try again.");
    }
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
    <SheetContent className="w-full border-l border-white/10 bg-[#081226] text-white sm:max-w-lg" data-testid="cart-sheet">
      <SheetHeader className="border-b border-white/10 pb-5">
        <SheetTitle className="font-display text-3xl text-[#f5f7ff]" data-testid="cart-sheet-title">
          Your private selection
        </SheetTitle>
        <SheetDescription data-testid="cart-sheet-description">
          Refined pieces saved for your next decision.
        </SheetDescription>
      </SheetHeader>

      <div className="mt-8 flex h-[calc(100vh-12rem)] flex-col justify-between gap-6">
        <div className="space-y-4 overflow-y-auto pr-2">
          {cartItems.length === 0 ? (
            <div className="rounded-[28px] border border-dashed border-[#d8b85d]/30 bg-white/5 p-6" data-testid="cart-empty-state">
              <p className="font-display text-2xl text-[#f5f7ff]">Your cart is beautifully empty.</p>
              <p className="mt-2 text-sm text-[#c9d1eb]">Add rings, grillz, and signature favorites from the shop.</p>
            </div>
          ) : (
            cartItems.map((item) => (
              <div
                key={item.lineId}
                className="grid grid-cols-[88px_1fr] gap-4 rounded-[28px] border border-white/10 bg-white/5 p-4"
                data-testid={`cart-item-${item.slug}`}
              >
                <img
                  src={item.hero_image}
                  alt={item.name}
                  className="h-24 w-24 rounded-[20px] object-cover"
                  data-testid={`cart-item-image-${item.slug}`}
                />
                <div className="space-y-3">
                  <div>
                    <p className="font-display text-2xl leading-none text-[#f5f7ff]" data-testid={`cart-item-name-${item.slug}`}>
                      {item.name}
                    </p>
                    <p className="mt-1 text-xs uppercase tracking-[0.24em] text-[#c6cff0]" data-testid={`cart-item-material-${item.slug}`}>
                      {item.material}
                    </p>
                    <p className="mt-2 text-sm text-[#d8b85d]" data-testid={`cart-item-price-${item.slug}`}>
                      {formatMoney(item.price)}
                    </p>
                  </div>

                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-2 rounded-full border border-white/10 bg-[#132247] px-2 py-1">
                      <button
                        type="button"
                        className="h-8 w-8 rounded-full text-lg text-[#f5f7ff] transition hover:bg-white/10"
                        onClick={() => updateCartQuantity(item.lineId, item.quantity - 1)}
                        data-testid={`cart-decrease-${item.slug}`}
                      >
                        −
                      </button>
                      <span className="min-w-6 text-center text-sm" data-testid={`cart-quantity-${item.slug}`}>
                        {item.quantity}
                      </span>
                      <button
                        type="button"
                        className="h-8 w-8 rounded-full text-lg text-[#f5f7ff] transition hover:bg-white/10"
                        onClick={() => updateCartQuantity(item.lineId, item.quantity + 1)}
                        data-testid={`cart-increase-${item.slug}`}
                      >
                        +
                      </button>
                    </div>

                    <button
                      type="button"
                      className="text-xs uppercase tracking-[0.22em] text-[#d8b85d] transition hover:text-white"
                      onClick={() => removeFromCart(item.lineId)}
                      data-testid={`cart-remove-${item.slug}`}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="space-y-3 border-t border-white/10 pt-6">
          <div className="flex items-center justify-between text-sm uppercase tracking-[0.24em] text-[#c6cff0]">
            <span data-testid="cart-subtotal-label">Estimated subtotal</span>
            <span className="font-medium text-[#f5f7ff]" data-testid="cart-subtotal-value">{formatMoney(subtotal)}</span>
          </div>
          <Button
            type="button"
            onClick={handleCheckout}
            disabled={cartItems.length === 0 || isRedirecting}
            className="h-12 w-full rounded-full bg-[#d8b85d] text-sm uppercase tracking-[0.18em] text-[#081226] transition hover:bg-[#f0d78d] disabled:opacity-50"
            data-testid="cart-checkout-button"
          >
            {isRedirecting ? "Redirecting to secure checkout…" : "Proceed to checkout"}
          </Button>
          <p className="text-center text-xs text-[#9aa6cf]" data-testid="cart-secure-note">
            Secure payment & checkout.
          </p>
          <div className="grid gap-3 sm:grid-cols-2">
            <SheetClose asChild>
              <Button asChild variant="outline" className="h-11 rounded-full border-[#d8b85d]/40 bg-transparent text-[#f5f7ff] hover:bg-white/10" data-testid="cart-continue-shopping-button">
                <Link to="/shop">Continue shopping</Link>
              </Button>
            </SheetClose>
            <SheetClose asChild>
              <Button asChild variant="outline" className="h-11 rounded-full border-[#d8b85d]/40 bg-transparent text-[#f5f7ff] hover:bg-white/10" data-testid="cart-bespoke-button">
                <Link to="/bespoke">Request concierge</Link>
              </Button>
            </SheetClose>
          </div>
        </div>
      </div>
    </SheetContent>
  </Sheet>
  );
};

import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button";
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
}) => (
  <Sheet open={open} onOpenChange={onOpenChange}>
    <SheetContent className="w-full border-l border-white/40 bg-[#fdfbf7] sm:max-w-lg" data-testid="cart-sheet">
      <SheetHeader className="border-b border-[#e7e1d7] pb-5">
        <SheetTitle className="font-display text-3xl text-[#0a0a0a]" data-testid="cart-sheet-title">
          Your private selection
        </SheetTitle>
        <SheetDescription data-testid="cart-sheet-description">
          Refined pieces saved for your next decision.
        </SheetDescription>
      </SheetHeader>

      <div className="mt-8 flex h-[calc(100vh-12rem)] flex-col justify-between gap-6">
        <div className="space-y-4 overflow-y-auto pr-2">
          {cartItems.length === 0 ? (
            <div className="rounded-[28px] border border-dashed border-[#cab995] bg-white/80 p-6" data-testid="cart-empty-state">
              <p className="font-display text-2xl text-[#0a0a0a]">Your cart is beautifully empty.</p>
              <p className="mt-2 text-sm text-[#666666]">Add rings, pearls, and bespoke favorites from the shop.</p>
            </div>
          ) : (
            cartItems.map((item) => (
              <div
                key={item.lineId}
                className="grid grid-cols-[88px_1fr] gap-4 rounded-[28px] border border-[#e7e1d7] bg-white/90 p-4"
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
                    <p className="font-display text-2xl leading-none text-[#0a0a0a]" data-testid={`cart-item-name-${item.slug}`}>
                      {item.name}
                    </p>
                    <p className="mt-1 text-xs uppercase tracking-[0.24em] text-[#666666]" data-testid={`cart-item-material-${item.slug}`}>
                      {item.material}
                    </p>
                    <p className="mt-2 text-sm text-[#022b22]" data-testid={`cart-item-price-${item.slug}`}>
                      {formatMoney(item.price)}
                    </p>
                  </div>

                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-2 rounded-full border border-[#d9cdb6] px-2 py-1">
                      <button
                        type="button"
                        className="h-8 w-8 rounded-full text-lg text-[#0a0a0a] transition hover:bg-[#f3ede2]"
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
                        className="h-8 w-8 rounded-full text-lg text-[#0a0a0a] transition hover:bg-[#f3ede2]"
                        onClick={() => updateCartQuantity(item.lineId, item.quantity + 1)}
                        data-testid={`cart-increase-${item.slug}`}
                      >
                        +
                      </button>
                    </div>

                    <button
                      type="button"
                      className="text-xs uppercase tracking-[0.22em] text-[#7d5f2d] transition hover:text-[#0a0a0a]"
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

        <div className="space-y-4 border-t border-[#e7e1d7] pt-6">
          <div className="flex items-center justify-between text-sm uppercase tracking-[0.24em] text-[#666666]">
            <span data-testid="cart-subtotal-label">Estimated subtotal</span>
            <span className="font-medium text-[#0a0a0a]" data-testid="cart-subtotal-value">{formatMoney(subtotal)}</span>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <SheetClose asChild>
              <Button asChild className="h-11 rounded-full bg-[#022b22] text-white hover:bg-[#0a0a0a]" data-testid="cart-continue-shopping-button">
                <Link to="/shop">Continue shopping</Link>
              </Button>
            </SheetClose>
            <SheetClose asChild>
              <Button asChild variant="outline" className="h-11 rounded-full border-[#cab995] bg-transparent hover:bg-[#f3ede2]" data-testid="cart-bespoke-button">
                <Link to="/bespoke">Request concierge</Link>
              </Button>
            </SheetClose>
          </div>
        </div>
      </div>
    </SheetContent>
  </Sheet>
);

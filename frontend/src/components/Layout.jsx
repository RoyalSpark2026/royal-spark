import { Gem, Heart, Menu, ShoppingBag } from "lucide-react";
import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";

import { CartSheet } from "@/components/CartSheet";

const navItems = [
  { to: "/", label: "Home" },
  { to: "/shop", label: "Shop" },
  { to: "/bespoke", label: "Bespoke" },
];

export const Layout = ({ storefront }) => {
  const [cartOpen, setCartOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.18),_transparent_34%),linear-gradient(180deg,_#fdfbf7_0%,_#fbf6ee_100%)] text-[#1a1a1a]" data-testid="app-shell">
      <header className="sticky top-0 z-40 border-b border-white/60 bg-white/70 backdrop-blur-xl" data-testid="site-header">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4 md:px-10 lg:px-16">
          <NavLink to="/" className="flex items-center gap-3 text-[#0a0a0a]" data-testid="brand-home-link">
            <span className="flex h-11 w-11 items-center justify-center rounded-full border border-[#d8c5a0] bg-white/80">
              <Gem className="h-5 w-5 text-[#7d5f2d]" />
            </span>
            <div>
              <p className="font-display text-3xl leading-none">Maison Aurelle</p>
              <p className="text-[10px] uppercase tracking-[0.32em] text-[#666666]" data-testid="brand-tagline">Fine jewelry atelier</p>
            </div>
          </NavLink>

          <button
            type="button"
            className="inline-flex h-11 w-11 items-center justify-center rounded-full border border-[#d9cdb6] text-[#0a0a0a] md:hidden"
            onClick={() => setMenuOpen((current) => !current)}
            data-testid="mobile-menu-button"
          >
            <Menu className="h-5 w-5" />
          </button>

          <nav className={`${menuOpen ? "flex" : "hidden"} absolute left-0 top-full w-full flex-col gap-2 border-b border-white/70 bg-[#fdfbf7] px-6 py-4 md:static md:flex md:w-auto md:flex-row md:border-none md:bg-transparent md:p-0`} data-testid="main-navigation">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={() => setMenuOpen(false)}
                className={({ isActive }) =>
                  `rounded-full px-4 py-2 text-sm uppercase tracking-[0.24em] transition ${
                    isActive ? "bg-[#022b22] text-white" : "text-[#534d45] hover:bg-white"
                  }`
                }
                data-testid={`nav-link-${item.label.toLowerCase()}`}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="hidden items-center gap-3 md:flex">
            <div className="inline-flex items-center gap-2 rounded-full border border-[#e7e1d7] bg-white/70 px-4 py-2 text-xs uppercase tracking-[0.22em] text-[#534d45]" data-testid="wishlist-count-chip">
              <Heart className="h-4 w-4" /> {storefront.wishlistIds.length} wished
            </div>
            <button
              type="button"
              className="inline-flex items-center gap-2 rounded-full bg-[#022b22] px-5 py-3 text-sm text-white transition hover:bg-[#0a0a0a]"
              onClick={() => setCartOpen(true)}
              data-testid="open-cart-button"
            >
              <ShoppingBag className="h-4 w-4" /> {storefront.cartCount} in cart
            </button>
          </div>
        </div>
      </header>

      <main data-testid="page-content">
        <Outlet context={storefront} />
      </main>

      <footer className="border-t border-[#e7e1d7] bg-white/60" data-testid="site-footer">
        <div className="mx-auto grid max-w-7xl gap-6 px-6 py-10 md:grid-cols-3 md:px-10 lg:px-16">
          <div>
            <p className="font-display text-3xl text-[#0a0a0a]" data-testid="footer-brand">Maison Aurelle</p>
            <p className="mt-3 max-w-sm text-sm leading-relaxed text-[#666666]" data-testid="footer-description">
              An editorial jewelry storefront built for timeless shopping and bespoke commissions.
            </p>
          </div>
          <div className="text-sm text-[#4f4a43]">
            <p className="text-xs uppercase tracking-[0.24em] text-[#7d5f2d]" data-testid="footer-services-label">Services</p>
            <p className="mt-3" data-testid="footer-services-content">Fine jewelry, bridal pieces, custom commissions, private sourcing.</p>
          </div>
          <div className="text-sm text-[#4f4a43]">
            <p className="text-xs uppercase tracking-[0.24em] text-[#7d5f2d]" data-testid="footer-contact-label">Contact</p>
            <p className="mt-3" data-testid="footer-contact-content">Concierge replies within one business day.</p>
          </div>
        </div>
      </footer>

      <button
        type="button"
        className="fixed bottom-5 right-5 inline-flex items-center gap-2 rounded-full bg-[#022b22] px-5 py-3 text-sm text-white shadow-lg transition hover:bg-[#0a0a0a] md:hidden"
        onClick={() => setCartOpen(true)}
        data-testid="mobile-open-cart-button"
      >
        <ShoppingBag className="h-4 w-4" /> {storefront.cartCount}
      </button>

      <CartSheet
        open={cartOpen}
        onOpenChange={setCartOpen}
        cartItems={storefront.cartItems}
        subtotal={storefront.subtotal}
        updateCartQuantity={storefront.updateCartQuantity}
        removeFromCart={storefront.removeFromCart}
      />
    </div>
  );
};

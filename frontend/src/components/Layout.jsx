import { Heart, Menu, ShoppingBag } from "lucide-react";
import { useState } from "react";
import { Link, NavLink, Outlet } from "react-router-dom";

import { CartSheet } from "@/components/CartSheet";

const fullLogo = "/royal-spark-logo-better.png";

const navItems = [
  { to: "/", label: "Home" },
  { to: "/shop", label: "Shop" },
  { to: "/bespoke", label: "Bespoke" },
  { to: "/contact", label: "Contact" },
];

const categoryItems = [
  { label: "Chains", href: "/shop?category=Chains" },
  { label: "Bangles", href: "/shop?category=Bangles" },
  { label: "Grillz", href: "/shop?category=Grills" },
  { label: "Charms", href: "/shop?category=Charms" },
  { label: "Rings", href: "/shop?category=Rings" },
  { label: "Earrings", href: "/shop?category=Earrings" },
  { label: "Bracelets", href: "/shop?category=Bracelets" },
  { label: "Moissanite", href: "/shop?material=Moissanite" },
  { label: "Contact", href: "/contact" },
];

export const Layout = ({ storefront }) => {
  const [cartOpen, setCartOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_right,_rgba(64,112,255,0.18),_transparent_26%),linear-gradient(180deg,_#081226_0%,_#101a33_100%)] text-[#f3f5ff]" data-testid="app-shell">
      <header className="sticky top-0 z-40 border-b border-white/10 bg-[#081226]/80 backdrop-blur-xl" data-testid="site-header">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4 md:px-10 lg:px-16">
          <NavLink to="/" className="flex items-center text-white" data-testid="brand-home-link">
            <div className="overflow-hidden rounded-[18px] border border-[#d8b85d]/20 bg-transparent px-2 py-2" data-testid="header-logo-image-wrapper">
              <img src={fullLogo} alt="Royal Spark logo" className="h-20 w-auto object-contain" data-testid="header-logo-image" />
            </div>
          </NavLink>

          <button
            type="button"
            className="inline-flex h-11 w-11 items-center justify-center rounded-full border border-white/15 text-white md:hidden"
            onClick={() => setMenuOpen((current) => !current)}
            data-testid="mobile-menu-button"
          >
            <Menu className="h-5 w-5" />
          </button>

          <nav className={`${menuOpen ? "flex" : "hidden"} absolute left-0 top-full w-full flex-col gap-2 border-b border-white/10 bg-[#0f1b37] px-6 py-4 md:static md:flex md:w-auto md:flex-row md:items-center md:border-none md:bg-transparent md:p-0`} data-testid="main-navigation">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={() => setMenuOpen(false)}
                className={({ isActive }) =>
                  `rounded-full px-4 py-2 text-sm uppercase tracking-[0.24em] transition ${
                    isActive ? "bg-[#d8b85d] text-[#081226]" : "text-[#d8def7] hover:bg-white/10"
                  }`
                }
                data-testid={`nav-link-${item.label.toLowerCase()}`}
              >
                {item.label}
              </NavLink>
            ))}
            <div className="mt-3 rounded-[24px] border border-white/10 bg-white/5 p-4 text-sm text-[#e9edff] md:hidden" data-testid="mobile-header-contact-card">
              <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]">Contact</p>
              <p className="mt-2" data-testid="mobile-header-phone">+1 832 329 7145</p>
              <p className="mt-1" data-testid="mobile-header-address">Sharps Town Plaza, Houston, Texas, USA</p>
            </div>
          </nav>

          <div className="hidden items-center gap-3 md:flex">
            <div className="rounded-[24px] border border-white/10 bg-white/5 px-4 py-3 text-right text-xs uppercase tracking-[0.16em] text-[#f0f3ff]" data-testid="header-contact-card">
              <p data-testid="header-phone">+1 832 329 7145</p>
            </div>
            <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.22em] text-[#dfe5ff]" data-testid="wishlist-count-chip">
              <Heart className="h-4 w-4" /> {storefront.wishlistIds.length} wished
            </div>
            <button
              type="button"
              className="inline-flex items-center gap-2 rounded-full bg-[#d8b85d] px-5 py-3 text-sm text-[#081226] transition hover:bg-[#f0d78d]"
              onClick={() => setCartOpen(true)}
              data-testid="open-cart-button"
            >
              <ShoppingBag className="h-4 w-4" /> {storefront.cartCount} in cart
            </button>
          </div>
        </div>

        <div className="border-t border-white/5 bg-[#0d1835]/90" data-testid="category-header-bar">
          <div className="mx-auto flex max-w-7xl gap-3 overflow-x-auto px-6 py-3 md:px-10 lg:px-16" data-testid="category-header-scroll-row">
            {categoryItems.map((item) => (
              <Link
                key={item.label}
                to={item.href}
                className="shrink-0 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.24em] text-[#dfe5ff] transition hover:border-[#d8b85d]/40 hover:bg-white/10 hover:text-[#d8b85d]"
                data-testid={`header-category-link-${item.label.toLowerCase()}`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </header>

      <main data-testid="page-content">
        <Outlet context={storefront} />
      </main>

      <footer className="border-t border-white/10 bg-[#081226]/70" data-testid="site-footer">
        <div className="mx-auto grid max-w-7xl gap-6 px-6 py-10 md:grid-cols-3 md:px-10 lg:px-16">
          <div className="flex flex-col gap-4">
            <div className="w-fit overflow-hidden rounded-[24px] border border-[#d8b85d]/20 bg-transparent px-2 py-2" data-testid="footer-logo-image-wrapper">
              <img src={fullLogo} alt="Royal Spark Jewelry logo" className="h-20 w-auto object-contain" data-testid="footer-logo-image" />
            </div>
            <p className="mt-3 max-w-sm text-sm leading-relaxed text-[#c6cff0]" data-testid="footer-description">
              A cinematic luxury storefront shaped by the Royal Spark brand film, premium craftsmanship, and a Shopify-ready catalog launch.
            </p>
          </div>
          <div className="text-sm text-[#e1e6ff]">
            <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]" data-testid="footer-services-label">Services</p>
            <p className="mt-3" data-testid="footer-services-content">Diamond rings, grillz, chains, bracelets, custom commissions.</p>
          </div>
          <div className="text-sm text-[#e1e6ff]">
            <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]" data-testid="footer-contact-label">Contact</p>
            <p className="mt-3" data-testid="footer-contact-phone">+1 832 329 7145</p>
            <p className="mt-2" data-testid="footer-contact-address">Sharps Town Plaza, Houston, Texas, USA</p>
          </div>
        </div>
      </footer>

      <button
        type="button"
        className="fixed bottom-5 right-5 inline-flex items-center gap-2 rounded-full bg-[#d8b85d] px-5 py-3 text-sm text-[#081226] shadow-lg shadow-[#071126]/40 transition hover:bg-[#f0d78d] md:hidden"
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

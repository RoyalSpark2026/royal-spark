import { ChevronDown, Gem, Heart, Menu, ShoppingBag } from "lucide-react";
import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";

import { CartSheet } from "@/components/CartSheet";

const fullLogo = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/ytwf02jq_IMG_7015.jpeg";

const navItems = [
  { to: "/", label: "Home" },
  { to: "/bespoke", label: "Bespoke" },
  { to: "/contact", label: "Contact" },
];

const categoryItems = [
  { label: "Chains", to: "/shop" },
  { label: "Bangles", to: "/shop" },
  { label: "Grillz", to: "/shop" },
  { label: "Charms", to: "/shop" },
  { label: "Rings", to: "/shop" },
  { label: "Earrings", to: "/shop" },
  { label: "Bracelets", to: "/shop" },
  { label: "Moissanite", to: "/shop" },
];

export const Layout = ({ storefront }) => {
  const [cartOpen, setCartOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileShopOpen, setMobileShopOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_right,_rgba(64,112,255,0.18),_transparent_26%),linear-gradient(180deg,_#081226_0%,_#101a33_100%)] text-[#f3f5ff]" data-testid="app-shell">
      <header className="sticky top-0 z-40 border-b border-white/10 bg-[#081226]/80 backdrop-blur-xl" data-testid="site-header">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4 md:px-10 lg:px-16">
          <NavLink to="/" className="flex items-center gap-3 text-white" data-testid="brand-home-link">
            <div className="overflow-hidden rounded-[18px] border border-[#d8b85d]/30 bg-black shadow-[0_0_28px_rgba(78,126,255,0.2)]" data-testid="header-logo-image-wrapper">
              <img src={fullLogo} alt="Royal Spark logo" className="h-14 w-14 object-cover object-top" data-testid="header-logo-image" />
            </div>
            <div>
              <p className="font-display text-3xl leading-none text-[#f5f7ff]" data-testid="brand-name">Royal Spark</p>
              <p className="text-[10px] uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="brand-tagline">Diamond rings & grillz studio</p>
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
            <div className="hidden md:block md:relative md:group" data-testid="desktop-shop-mega-menu-wrapper">
              <NavLink
                to="/shop"
                className={({ isActive }) => `rounded-full px-4 py-2 text-sm uppercase tracking-[0.24em] transition ${isActive ? "bg-[#d8b85d] text-[#081226]" : "text-[#d8def7] hover:bg-white/10"}`}
                data-testid="nav-link-shop"
              >
                <span className="inline-flex items-center gap-2">
                  Shop <ChevronDown className="h-4 w-4" />
                </span>
              </NavLink>

              <div className="invisible absolute left-1/2 top-full z-50 mt-4 w-[520px] -translate-x-1/2 rounded-[28px] border border-white/10 bg-[#111d3a]/95 p-6 opacity-0 shadow-2xl shadow-black/30 backdrop-blur transition duration-200 group-hover:visible group-hover:opacity-100" data-testid="desktop-shop-mega-menu-panel">
                <div className="mb-4 flex items-center justify-between">
                  <p className="text-xs uppercase tracking-[0.28em] text-[#d8b85d]" data-testid="desktop-shop-mega-menu-title">Browse categories</p>
                  <NavLink to="/shop" className="text-xs uppercase tracking-[0.24em] text-[#d8def7]" data-testid="desktop-shop-mega-menu-all-link">View all</NavLink>
                </div>
                <div className="grid grid-cols-2 gap-3" data-testid="desktop-shop-mega-menu-grid">
                  {categoryItems.map((item) => (
                    <NavLink
                      key={item.label}
                      to={item.to}
                      className="rounded-[18px] border border-white/10 bg-white/5 px-4 py-3 text-sm uppercase tracking-[0.18em] text-[#eef2ff] transition hover:border-[#d8b85d]/40 hover:text-[#d8b85d]"
                      data-testid={`desktop-mega-menu-item-${item.label.toLowerCase()}`}
                    >
                      {item.label}
                    </NavLink>
                  ))}
                </div>
              </div>
            </div>

            <div className="md:hidden" data-testid="mobile-shop-mega-menu-wrapper">
              <button
                type="button"
                className="flex w-full items-center justify-between rounded-full px-4 py-2 text-sm uppercase tracking-[0.24em] text-[#d8def7] transition hover:bg-white/10"
                onClick={() => setMobileShopOpen((current) => !current)}
                data-testid="mobile-shop-menu-toggle"
              >
                <span>Shop</span>
                <ChevronDown className={`h-4 w-4 transition ${mobileShopOpen ? "rotate-180" : ""}`} />
              </button>

              {mobileShopOpen ? (
                <div className="mt-3 grid gap-2 rounded-[24px] border border-white/10 bg-white/5 p-4" data-testid="mobile-shop-menu-panel">
                  <NavLink
                    to="/shop"
                    onClick={() => setMenuOpen(false)}
                    className="rounded-[16px] border border-white/10 px-4 py-3 text-xs uppercase tracking-[0.24em] text-[#d8b85d]"
                    data-testid="mobile-shop-menu-all-link"
                  >
                    View all collections
                  </NavLink>
                  {categoryItems.map((item) => (
                    <NavLink
                      key={item.label}
                      to={item.to}
                      onClick={() => setMenuOpen(false)}
                      className="rounded-[16px] border border-white/10 px-4 py-3 text-xs uppercase tracking-[0.24em] text-[#eef2ff]"
                      data-testid={`mobile-mega-menu-item-${item.label.toLowerCase()}`}
                    >
                      {item.label}
                    </NavLink>
                  ))}
                </div>
              ) : null}
            </div>

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
      </header>

      <main data-testid="page-content">
        <Outlet context={storefront} />
      </main>

      <footer className="border-t border-white/10 bg-[#081226]/70" data-testid="site-footer">
        <div className="mx-auto grid max-w-7xl gap-6 px-6 py-10 md:grid-cols-3 md:px-10 lg:px-16">
          <div className="flex flex-col gap-4">
            <div className="w-fit overflow-hidden rounded-[24px] border border-[#d8b85d]/30 bg-black" data-testid="footer-logo-image-wrapper">
              <img src={fullLogo} alt="Royal Spark Jewelry logo" className="h-28 w-28 object-cover object-top" data-testid="footer-logo-image" />
            </div>
            <p className="font-display text-3xl text-[#f5f7ff]" data-testid="footer-brand">Royal Spark</p>
            <p className="mt-3 max-w-sm text-sm leading-relaxed text-[#c6cff0]" data-testid="footer-description">
              A blue-label storefront for diamond rings, custom grillz, and high-visibility showroom styling.
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

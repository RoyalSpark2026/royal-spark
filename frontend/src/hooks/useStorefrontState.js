import { useEffect, useMemo, useState } from "react";

const CART_KEY = "maison-aurelle-cart";
const WISHLIST_KEY = "maison-aurelle-wishlist";

const readStoredValue = (key, fallback) => {
  try {
    const value = window.localStorage.getItem(key);
    return value ? JSON.parse(value) : fallback;
  } catch {
    return fallback;
  }
};

export const useStorefrontState = () => {
  const [cartItems, setCartItems] = useState(() => readStoredValue(CART_KEY, []));
  const [wishlistIds, setWishlistIds] = useState(() => readStoredValue(WISHLIST_KEY, []));

  useEffect(() => {
    window.localStorage.setItem(CART_KEY, JSON.stringify(cartItems));
  }, [cartItems]);

  useEffect(() => {
    window.localStorage.setItem(WISHLIST_KEY, JSON.stringify(wishlistIds));
  }, [wishlistIds]);

  const addToCart = (product, material) => {
    const chosenMaterial = material || product.materials?.[0] || "Signature";
    const lineId = `${product.id}-${chosenMaterial}`;

    setCartItems((currentItems) => {
      const existingItem = currentItems.find((item) => item.lineId === lineId);
      if (existingItem) {
        return currentItems.map((item) =>
          item.lineId === lineId ? { ...item, quantity: item.quantity + 1 } : item,
        );
      }

      return [
        ...currentItems,
        {
          lineId,
          id: product.id,
          slug: product.slug,
          name: product.name,
          price: product.price,
          variant_id: product.variant_id || null,
          hero_image: product.hero_image,
          material: chosenMaterial,
          quantity: 1,
        },
      ];
    });
  };

  const toggleWishlist = (productId) => {
    setWishlistIds((currentIds) =>
      currentIds.includes(productId)
        ? currentIds.filter((id) => id !== productId)
        : [...currentIds, productId],
    );
  };

  const updateCartQuantity = (lineId, quantity) => {
    if (quantity <= 0) {
      setCartItems((currentItems) => currentItems.filter((item) => item.lineId !== lineId));
      return;
    }

    setCartItems((currentItems) =>
      currentItems.map((item) => (item.lineId === lineId ? { ...item, quantity } : item)),
    );
  };

  const removeFromCart = (lineId) => {
    setCartItems((currentItems) => currentItems.filter((item) => item.lineId !== lineId));
  };

  const cartCount = useMemo(
    () => cartItems.reduce((total, item) => total + item.quantity, 0),
    [cartItems],
  );

  const subtotal = useMemo(
    () => cartItems.reduce((total, item) => total + item.price * item.quantity, 0),
    [cartItems],
  );

  return {
    cartItems,
    wishlistIds,
    addToCart,
    toggleWishlist,
    updateCartQuantity,
    removeFromCart,
    cartCount,
    subtotal,
  };
};

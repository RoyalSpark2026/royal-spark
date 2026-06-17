import { ThemeProvider } from "next-themes";
import "@/App.css";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { Layout } from "@/components/Layout";
import { Toaster } from "@/components/ui/sonner";
import { useStorefrontState } from "@/hooks/useStorefrontState";
import BespokePage from "@/pages/BespokePage";
import ContactPage from "@/pages/ContactPage";
import HomePage from "@/pages/HomePage";
import ProductDetailPage from "@/pages/ProductDetailPage";
import ShopPage from "@/pages/ShopPage";

function App() {
  const storefront = useStorefrontState();

  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout storefront={storefront} />}>
              <Route index element={<HomePage />} />
              <Route path="shop" element={<ShopPage />} />
              <Route path="shop/:slug" element={<ProductDetailPage />} />
              <Route path="bespoke" element={<BespokePage />} />
              <Route path="contact" element={<ContactPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </BrowserRouter>
        <Toaster richColors position="top-right" />
      </div>
    </ThemeProvider>
  );
}

export default App;

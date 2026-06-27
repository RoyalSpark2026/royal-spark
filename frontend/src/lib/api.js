import axios from "axios";

const api = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_URL}/api`,
});

export const fetchHomeData = async () => {
  const response = await api.get("/catalog/home");
  return response.data;
};

export const fetchProducts = async (params = {}) => {
  const response = await api.get("/catalog/products", { params });
  return response.data;
};

export const fetchProductDetail = async (slug) => {
  const response = await api.get(`/catalog/products/${slug}`);
  return response.data;
};

export const submitBespokeInquiry = async (payload) => {
  const response = await api.post("/bespoke-inquiries", payload);
  return response.data;
};

export const fetchShopifyReadiness = async () => {
  const response = await api.get("/shopify/readiness");
  return response.data;
};

export const createCheckout = async (items) => {
  const response = await api.post("/checkout", { items });
  return response.data;
};

import axios from 'axios';
import { Product, ProductWithHistory, PriceHistory, ProductCreate } from './types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const productApi = {
  // Get all products
  getAllProducts: async (): Promise<Product[]> => {
    const response = await api.get('/products/');
    return response.data;
  },

  // Get a specific product with price history
  getProductWithHistory: async (productId: number): Promise<ProductWithHistory> => {
    const response = await api.get(`/products/${productId}`);
    return response.data;
  },

  // Create a new product
  createProduct: async (productData: ProductCreate): Promise<Product> => {
    const response = await api.post('/products/', productData);
    return response.data;
  },

  // Update product price
  updateProductPrice: async (productId: number): Promise<Product> => {
    const response = await api.post(`/products/${productId}/update`);
    return response.data;
  },

  // Delete a product
  deleteProduct: async (productId: number): Promise<void> => {
    await api.delete(`/products/${productId}`);
  },

  // Get price history for a product
  getPriceHistory: async (productId: number): Promise<PriceHistory[]> => {
    const response = await api.get(`/products/${productId}/price-history`);
    return response.data;
  },
};


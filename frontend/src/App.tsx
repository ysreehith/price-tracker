import React, { useState, useEffect } from 'react';
import { Product, ProductWithHistory } from './types';
import { productApi } from './api';
import ProductForm from './components/ProductForm';
import ProductsTable from './components/ProductsTable';
import PriceChart from './components/PriceChart';

const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedProduct, setSelectedProduct] = useState<ProductWithHistory | null>(null);

  // Load products on component mount
  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const productsData = await productApi.getAllProducts();
      setProducts(productsData);
      setError(null);
    } catch (err: any) {
      setError('Failed to load products. Please check if the backend is running.');
      console.error('Error loading products:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleProductAdded = (newProduct: Product) => {
    setProducts(prev => [...prev, newProduct]);
  };

  const handleProductUpdated = (updatedProduct: Product) => {
    setProducts(prev =>
      prev.map(product =>
        product.id === updatedProduct.id ? updatedProduct : product
      )
    );
  };

  const handleProductDeleted = (productId: number) => {
    setProducts(prev => prev.filter(product => product.id !== productId));
  };

  const handleViewChart = async (productId: number) => {
    try {
      const productWithHistory = await productApi.getProductWithHistory(productId);
      setSelectedProduct(productWithHistory);
    } catch (err: any) {
      console.error('Error loading product history:', err);
      setError('Failed to load price history for this product.');
    }
  };

  const handleCloseChart = () => {
    setSelectedProduct(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading products...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Price Tracker</h1>
          <p className="text-gray-600">
            Track product prices from Amazon, eBay, and Walmart
          </p>
        </header>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
            <button
              onClick={loadProducts}
              className="ml-4 text-red-600 hover:text-red-800 underline"
            >
              Retry
            </button>
          </div>
        )}

        <div className="space-y-8">
          <ProductForm onProductAdded={handleProductAdded} />
          <ProductsTable
            products={products}
            onProductUpdated={handleProductUpdated}
            onProductDeleted={handleProductDeleted}
            onViewChart={handleViewChart}
          />
        </div>

        {selectedProduct && (
          <PriceChart
            productName={selectedProduct.product.name}
            priceHistory={selectedProduct.price_history}
            onClose={handleCloseChart}
          />
        )}
      </div>
    </div>
  );
};

export default App;


import React, { useState } from 'react';
import { Product } from '../types';
import { productApi } from '../api';

interface ProductsTableProps {
  products: Product[];
  onProductUpdated: (product: Product) => void;
  onProductDeleted: (productId: number) => void;
  onViewChart: (productId: number) => void;
}

const ProductsTable: React.FC<ProductsTableProps> = ({
  products,
  onProductUpdated,
  onProductDeleted,
  onViewChart,
}) => {
  const [updatingProducts, setUpdatingProducts] = useState<Set<number>>(new Set());
  const [deletingProducts, setDeletingProducts] = useState<Set<number>>(new Set());

  const handleUpdatePrice = async (productId: number) => {
    setUpdatingProducts(prev => new Set(prev).add(productId));
    
    try {
      const updatedProduct = await productApi.updateProductPrice(productId);
      onProductUpdated(updatedProduct);
    } catch (error) {
      console.error('Failed to update product price:', error);
    } finally {
      setUpdatingProducts(prev => {
        const newSet = new Set(prev);
        newSet.delete(productId);
        return newSet;
      });
    }
  };

  const handleDeleteProduct = async (productId: number) => {
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }

    setDeletingProducts(prev => new Set(prev).add(productId));
    
    try {
      await productApi.deleteProduct(productId);
      onProductDeleted(productId);
    } catch (error) {
      console.error('Failed to delete product:', error);
    } finally {
      setDeletingProducts(prev => {
        const newSet = new Set(prev);
        newSet.delete(productId);
        return newSet;
      });
    }
  };

  const formatPrice = (price: number | null) => {
    if (price === null) return 'N/A';
    return `$${price.toFixed(2)}`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getDomainFromUrl = (url: string) => {
    try {
      const domain = new URL(url).hostname;
      if (domain.includes('amazon')) return 'Amazon';
      if (domain.includes('ebay')) return 'eBay';
      if (domain.includes('walmart')) return 'Walmart';
      return domain;
    } catch {
      return 'Unknown';
    }
  };

  if (products.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Tracked Products</h2>
        <div className="text-center py-8">
          <p className="text-gray-500 text-lg">No products tracked yet.</p>
          <p className="text-gray-400">Add a product URL above to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Tracked Products</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Product
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Source
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Current Price
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Last Updated
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {products.map((product) => (
              <tr key={product.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900 max-w-xs truncate">
                    {product.name}
                  </div>
                  <div className="text-sm text-gray-500 max-w-xs truncate">
                    <a
                      href={product.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:text-primary-800"
                    >
                      View Product
                    </a>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {getDomainFromUrl(product.url)}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {formatPrice(product.current_price)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {formatDate(product.last_updated)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button
                    onClick={() => onViewChart(product.id)}
                    className="text-primary-600 hover:text-primary-900"
                  >
                    View Chart
                  </button>
                  <button
                    onClick={() => handleUpdatePrice(product.id)}
                    disabled={updatingProducts.has(product.id)}
                    className="text-green-600 hover:text-green-900 disabled:opacity-50"
                  >
                    {updatingProducts.has(product.id) ? 'Updating...' : 'Update'}
                  </button>
                  <button
                    onClick={() => handleDeleteProduct(product.id)}
                    disabled={deletingProducts.has(product.id)}
                    className="text-red-600 hover:text-red-900 disabled:opacity-50"
                  >
                    {deletingProducts.has(product.id) ? 'Deleting...' : 'Delete'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ProductsTable;


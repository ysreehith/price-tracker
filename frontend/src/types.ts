export interface Product {
  id: number;
  name: string;
  url: string;
  current_price: number | null;
  last_updated: string;
  created_at: string;
}

export interface PriceHistory {
  id: number;
  product_id: number;
  price: number;
  timestamp: string;
}

export interface ProductWithHistory {
  product: Product;
  price_history: PriceHistory[];
}

export interface ProductCreate {
  url: string;
}


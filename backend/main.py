from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db, create_tables, Product, PriceHistory
from models import ProductCreate, ProductResponse, PriceHistoryResponse, ProductWithHistory, ScrapeResult
from scraper import PriceScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Price Tracker API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://*.vercel.app",   # Vercel deployments
        "https://*.railway.app",  # Railway deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scraper
scraper = PriceScraper()

# Create database tables
create_tables()

@app.get("/")
async def root():
    return {"message": "Price Tracker API is running!"}

@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to track"""
    try:
        # Check if product already exists
        existing_product = db.query(Product).filter(Product.url == str(product.url)).first()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this URL already exists"
            )
        
        # Scrape product information
        scrape_result = scraper.scrape_product(str(product.url))
        
        if not scrape_result['success'] or not scrape_result['name']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to scrape product: {scrape_result.get('error', 'Unknown error')}"
            )
        
        # Create new product
        db_product = Product(
            name=scrape_result['name'],
            url=str(product.url),
            current_price=scrape_result['price']
        )
        
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        
        # Add initial price to history
        if scrape_result['price']:
            price_entry = PriceHistory(
                product_id=db_product.id,
                price=scrape_result['price']
            )
            db.add(price_entry)
            db.commit()
        
        logger.info(f"Created product: {db_product.name}")
        return db_product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/products/", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """Get all tracked products"""
    products = db.query(Product).all()
    return products

@app.get("/products/{product_id}", response_model=ProductWithHistory)
async def get_product_with_history(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product with its price history"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    price_history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).order_by(PriceHistory.timestamp.desc()).all()
    
    return ProductWithHistory(
        product=product,
        price_history=price_history
    )

@app.post("/products/{product_id}/update", response_model=ProductResponse)
async def update_product_price(product_id: int, db: Session = Depends(get_db)):
    """Update product price by scraping again"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    try:
        # Scrape current price
        scrape_result = scraper.scrape_product(product.url)
        
        if not scrape_result['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to scrape product: {scrape_result.get('error', 'Unknown error')}"
            )
        
        # Update product with new price
        if scrape_result['price']:
            product.current_price = scrape_result['price']
            product.last_updated = db.query(Product).filter(Product.id == product_id).first().last_updated
            
            # Add new price to history
            price_entry = PriceHistory(
                product_id=product_id,
                price=scrape_result['price']
            )
            db.add(price_entry)
            db.commit()
            db.refresh(product)
        
        logger.info(f"Updated product: {product.name} - New price: {product.current_price}")
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product and its price history"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    
    logger.info(f"Deleted product: {product.name}")
    return {"message": "Product deleted successfully"}

@app.get("/products/{product_id}/price-history", response_model=List[PriceHistoryResponse])
async def get_price_history(product_id: int, db: Session = Depends(get_db)):
    """Get price history for a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    price_history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).order_by(PriceHistory.timestamp.asc()).all()
    
    return price_history

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(app, host="0.0.0.0", port=port)


from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class ProductCreate(BaseModel):
    url: HttpUrl

class ProductResponse(BaseModel):
    id: int
    name: str
    url: str
    current_price: Optional[float]
    last_updated: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class PriceHistoryResponse(BaseModel):
    id: int
    product_id: int
    price: float
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ProductWithHistory(BaseModel):
    product: ProductResponse
    price_history: List[PriceHistoryResponse]

class ScrapeResult(BaseModel):
    name: Optional[str]
    price: Optional[float]
    success: bool
    error: Optional[str] = None


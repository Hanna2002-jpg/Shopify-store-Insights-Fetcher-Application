from pydantic import BaseModel
from typing import Optional, List, Dict, Any


# -------------------------------
# Request / Response Base Schemas
# -------------------------------
class ExtractRequest(BaseModel):
    """Schema for extract request payload"""
    website_url: str


class ErrorResponseSchema(BaseModel):
    """Schema for error responses"""
    detail: str


class BrandInsightsSchema(BaseModel):
    """Schema for successful brand insights response"""
    status: str
    brand_name: Optional[str]
    website_url: str
    data: Dict[str, Any]
    extraction_timestamp: str
    processing_time_seconds: float
    errors: Optional[List[str]] = []
    warnings: Optional[List[str]] = []


# -------------------------------
# Shopify Entities
# -------------------------------
class Product(BaseModel):
    id: Optional[int]
    title: str
    handle: Optional[str]
    description: Optional[str]
    price: Optional[str]
    images: Optional[List[str]] = []
    product_url: Optional[str]


class Collection(BaseModel):
    id: Optional[int]
    title: str
    handle: Optional[str]
    description: Optional[str]
    published_at: Optional[str]
    updated_at: Optional[str]
    image: Optional[str] = None
    products_count: Optional[int] = 0


class Policies(BaseModel):
    privacy_policy: Optional[str] = None
    return_policy: Optional[str] = None
    refund_policy: Optional[str] = None
    terms_of_service: Optional[str] = None


class SocialHandles(BaseModel):
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    tiktok: Optional[str] = None
    youtube: Optional[str] = None
    linkedin: Optional[str] = None


class ContactInfo(BaseModel):
    emails: List[str] = []
    phones: List[str] = []
    address: Optional[str] = None
    social_handles: Optional[SocialHandles] = None


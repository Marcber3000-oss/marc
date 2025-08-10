from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from enum import Enum


class BookCategory(str, Enum):
    DESARROLLO_PERSONAL = "Desarrollo Personal"
    PRODUCTIVIDAD = "Productividad"  
    CRECIMIENTO_PERSONAL = "Crecimiento Personal"
    LIDERAZGO = "Liderazgo"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    DELIVERED = "delivered"
    FAILED = "failed"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


# Book Models
class Book(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    author: str = "María Fernández"
    price: float
    originalPrice: float
    description: str
    category: BookCategory
    cover: str
    pages: int
    rating: float = 4.8
    reviewCount: int = 0
    bestseller: bool = False
    fileUrl: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class BookCreate(BaseModel):
    title: str
    price: float
    originalPrice: float
    description: str
    category: BookCategory
    cover: str
    pages: int
    bestseller: bool = False
    fileUrl: Optional[str] = None


# Customer Models
class CustomerInfo(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    country: str


# Order Models  
class OrderItem(BaseModel):
    bookId: str
    quantity: int = 1
    price: float
    title: str


class PaymentInfo(BaseModel):
    paymentIntentId: Optional[str] = None
    amount: float
    status: PaymentStatus = PaymentStatus.PENDING
    paymentMethod: Optional[str] = None


class DownloadLink(BaseModel):
    bookId: str
    bookTitle: str
    downloadUrl: str
    expiresAt: datetime


class Order(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    orderId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    items: List[OrderItem]
    customer: CustomerInfo
    paymentInfo: PaymentInfo
    downloadLinks: List[DownloadLink] = []
    status: OrderStatus = OrderStatus.PENDING
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class OrderCreate(BaseModel):
    items: List[OrderItem]
    customer: CustomerInfo


# Review Models
class Review(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    author: str
    title: str  # Professional title
    avatar: str
    review: str
    rating: int = 5
    bookId: Optional[str] = None
    bookTitle: str
    featured: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


# Author Models
class AuthorStats(BaseModel):
    booksPublished: int = 12
    readersReached: str = "500K+"
    averageRating: float = 4.8
    countries: int = 25


class SocialMedia(BaseModel):
    instagram: str = "@mariafernandezautor"
    facebook: str = "MariaFernandezLibros"
    linkedin: str = "maria-fernandez-autor"


class Author(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = "María Fernández"
    title: str = "Autora de Bestsellers en Desarrollo Personal"
    bio: str
    avatar: str
    achievements: List[str]
    socialMedia: SocialMedia = Field(default_factory=SocialMedia)
    stats: AuthorStats = Field(default_factory=AuthorStats)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


# Stripe Models
class PaymentIntentCreate(BaseModel):
    orderId: str
    amount: float


class PaymentIntentResponse(BaseModel):
    clientSecret: str
    paymentIntentId: str


class PaymentConfirm(BaseModel):
    paymentIntentId: str
    orderId: str


# Response Models
class BookListResponse(BaseModel):
    books: List[Book]
    total: int


class OrderResponse(BaseModel):
    orderId: str
    status: OrderStatus
    downloadLinks: List[DownloadLink] = []
    message: str


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
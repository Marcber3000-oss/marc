from fastapi import FastAPI, APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import List
import stripe

# Import our models and services
from models import (
    Book, BookListResponse, Order, OrderCreate, OrderResponse, 
    Review, Author, PaymentIntentCreate, PaymentIntentResponse, 
    PaymentConfirm, ApiResponse
)
from database import connect_to_mongo, close_mongo_connection
from services.book_service import BookService
from services.order_service import OrderService
from services.stripe_service import StripeService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(
    title="Ebooks API", 
    description="API for María Fernández's ebook store",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize services
book_service = BookService()
order_service = OrderService()
stripe_service = StripeService()

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    logging.info("Application started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    logging.info("Application shutdown complete")

# Root endpoint
@api_router.get("/")
async def root():
    return {"message": "Ebooks API is running", "version": "1.0.0"}

# Book endpoints
@api_router.get("/books", response_model=BookListResponse)
async def get_books():
    """Get all books"""
    try:
        books = await book_service.get_all_books()
        return BookListResponse(books=books, total=len(books))
    except Exception as e:
        logging.error(f"Error getting books: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@api_router.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """Get a specific book by ID"""
    try:
        book = await book_service.get_book_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return book
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@api_router.get("/books/category/{category}")
async def get_books_by_category(category: str):
    """Get books by category"""
    try:
        books = await book_service.get_books_by_category(category)
        return {"books": books, "total": len(books), "category": category}
    except Exception as e:
        logging.error(f"Error getting books by category {category}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@api_router.get("/books/featured/bestsellers")
async def get_bestsellers():
    """Get bestseller books"""
    try:
        books = await book_service.get_bestsellers()
        return {"books": books, "total": len(books)}
    except Exception as e:
        logging.error(f"Error getting bestsellers: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Include the router in the main app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

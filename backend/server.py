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

# Reviews endpoints
@api_router.get("/reviews")
async def get_reviews():
    """Get all featured reviews"""
    try:
        from database import get_database
        db = get_database()
        cursor = db.reviews.find({"featured": True})
        reviews_data = await cursor.to_list(length=None)
        
        reviews = []
        for review_data in reviews_data:
            review_data['_id'] = str(review_data['_id'])
            reviews.append(review_data)
        
        return {"reviews": reviews, "total": len(reviews)}
    except Exception as e:
        logging.error(f"Error getting reviews: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@api_router.get("/reviews/book/{book_title}")
async def get_book_reviews(book_title: str):
    """Get reviews for a specific book"""
    try:
        from database import get_database
        db = get_database()
        cursor = db.reviews.find({"bookTitle": book_title})
        reviews_data = await cursor.to_list(length=None)
        
        reviews = []
        for review_data in reviews_data:
            review_data['_id'] = str(review_data['_id'])
            reviews.append(review_data)
        
        return {"reviews": reviews, "total": len(reviews), "bookTitle": book_title}
    except Exception as e:
        logging.error(f"Error getting book reviews: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Author endpoint
@api_router.get("/author")
async def get_author():
    """Get author information"""
    try:
        from database import get_database
        db = get_database()
        author_data = await db.author.find_one({})
        
        if author_data:
            author_data['_id'] = str(author_data['_id'])
            return {"author": author_data}
        else:
            raise HTTPException(status_code=404, detail="Información del autor no encontrada")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting author: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Order endpoints
@api_router.post("/orders", response_model=OrderResponse)
async def create_order(order_data: OrderCreate):
    """Create a new order"""
    try:
        order = await order_service.create_order(order_data)
        return OrderResponse(
            orderId=order.orderId,
            status=order.status,
            message="Orden creada exitosamente"
        )
    except Exception as e:
        logging.error(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail="Error creando la orden")

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get order by ID"""
    try:
        order = await order_service.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        return order
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting order {order_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Payment endpoints (Stripe integration)
@api_router.post("/payments/create-intent")
async def create_payment_intent(payment_data: PaymentIntentCreate):
    """Create Stripe Payment Intent"""
    try:
        # Get order to verify amount
        order = await order_service.get_order_by_id(payment_data.orderId)
        if not order:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        
        # Create payment intent with Stripe
        result = await stripe_service.create_payment_intent(
            amount=payment_data.amount,
            order_id=payment_data.orderId,
            customer_email=order.customer.email
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Error creando intento de pago"))
        
        # Update order with payment intent ID
        await order_service.update_payment_info(
            payment_data.orderId,
            result["paymentIntentId"],
            "pending"
        )
        
        return PaymentIntentResponse(
            clientSecret=result["clientSecret"],
            paymentIntentId=result["paymentIntentId"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error creating payment intent: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@api_router.post("/payments/confirm")
async def confirm_payment(payment_confirm: PaymentConfirm):
    """Confirm payment and generate download links"""
    try:
        # Verify payment with Stripe
        payment_result = await stripe_service.confirm_payment(payment_confirm.paymentIntentId)
        
        if not payment_result["success"] or payment_result["status"] != "succeeded":
            raise HTTPException(status_code=400, detail="Pago no confirmado")
        
        # Update order status
        await order_service.update_payment_info(
            payment_confirm.orderId,
            payment_confirm.paymentIntentId,
            "completed"
        )
        
        # Generate download links
        order = await order_service.generate_download_links(payment_confirm.orderId)
        
        if not order:
            raise HTTPException(status_code=400, detail="Error generando enlaces de descarga")
        
        return {
            "success": True,
            "message": "Pago confirmado exitosamente",
            "downloadLinks": [link.model_dump() for link in order.downloadLinks]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error confirming payment: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Stripe configuration endpoint
@api_router.get("/config/stripe")
async def get_stripe_config():
    """Get Stripe publishable key"""
    return {
        "publishableKey": stripe_service.get_publishable_key()
    }

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

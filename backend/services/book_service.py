from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from models import Book, BookCreate
from database import get_database


class BookService:
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db or get_database()
        self.collection = self.db.books

    async def get_all_books(self) -> List[Book]:
        """Get all books"""
        cursor = self.collection.find({})
        books_data = await cursor.to_list(length=None)
        
        books = []
        for book_data in books_data:
            book_data['_id'] = str(book_data['_id'])
            books.append(Book(**book_data))
        
        return books

    async def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Get book by ID"""
        if not ObjectId.is_valid(book_id):
            return None
            
        book_data = await self.collection.find_one({"_id": ObjectId(book_id)})
        
        if book_data:
            book_data['_id'] = str(book_data['_id'])
            return Book(**book_data)
        
        return None

    async def get_books_by_category(self, category: str) -> List[Book]:
        """Get books by category"""
        cursor = self.collection.find({"category": category})
        books_data = await cursor.to_list(length=None)
        
        books = []
        for book_data in books_data:
            book_data['_id'] = str(book_data['_id'])
            books.append(Book(**book_data))
        
        return books

    async def get_bestsellers(self) -> List[Book]:
        """Get bestseller books"""
        cursor = self.collection.find({"bestseller": True})
        books_data = await cursor.to_list(length=None)
        
        books = []
        for book_data in books_data:
            book_data['_id'] = str(book_data['_id'])
            books.append(Book(**book_data))
        
        return books

    async def create_book(self, book_create: BookCreate) -> Book:
        """Create a new book"""
        book_data = book_create.model_dump()
        book_data['createdAt'] = book_data.get('createdAt') or datetime.utcnow()
        book_data['updatedAt'] = book_data.get('updatedAt') or datetime.utcnow()
        
        result = await self.collection.insert_one(book_data)
        book_data['_id'] = str(result.inserted_id)
        
        return Book(**book_data)

    async def update_book(self, book_id: str, book_update: dict) -> Optional[Book]:
        """Update a book"""
        if not ObjectId.is_valid(book_id):
            return None
            
        book_update['updatedAt'] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {"$set": book_update},
            return_document=True
        )
        
        if result:
            result['_id'] = str(result['_id'])
            return Book(**result)
        
        return None

    async def delete_book(self, book_id: str) -> bool:
        """Delete a book"""
        if not ObjectId.is_valid(book_id):
            return False
            
        result = await self.collection.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0

    async def get_book_stats(self) -> dict:
        """Get book statistics"""
        total_books = await self.collection.count_documents({})
        bestsellers = await self.collection.count_documents({"bestseller": True})
        
        # Calculate average rating
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "averageRating": {"$avg": "$rating"},
                    "totalReviews": {"$sum": "$reviewCount"}
                }
            }
        ]
        
        cursor = self.collection.aggregate(pipeline)
        stats = await cursor.to_list(length=1)
        
        if stats:
            avg_rating = round(stats[0]['averageRating'], 1)
            total_reviews = stats[0]['totalReviews']
        else:
            avg_rating = 4.8
            total_reviews = 0
        
        return {
            "totalBooks": total_books,
            "bestsellers": bestsellers,
            "averageRating": avg_rating,
            "totalReviews": total_reviews
        }
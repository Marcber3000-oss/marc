import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

database = Database()

async def connect_to_mongo():
    """Create database connection"""
    try:
        mongo_url = os.environ['MONGO_URL']
        database.client = AsyncIOMotorClient(mongo_url)
        database.database = database.client[os.environ['DB_NAME']]
        
        # Test the connection
        await database.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Initialize collections with sample data if empty
        await initialize_sample_data()
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection"""
    if database.client:
        database.client.close()
        logger.info("Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return database.database

async def initialize_sample_data():
    """Initialize database with sample data if collections are empty"""
    db = get_database()
    
    try:
        # Initialize Books
        books_count = await db.books.count_documents({})
        if books_count == 0:
            sample_books = [
                {
                    "title": "El Poder de la Mentalidad Positiva",
                    "author": "María Fernández",
                    "price": 19.99,
                    "originalPrice": 24.99,
                    "rating": 4.8,
                    "reviewCount": 156,
                    "cover": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
                    "description": "Descubre cómo transformar tu vida a través del poder de los pensamientos positivos y la mentalidad ganadora.",
                    "category": "Desarrollo Personal",
                    "pages": 256,
                    "bestseller": True,
                    "fileUrl": "https://example.com/books/mentalidad-positiva.pdf"
                },
                {
                    "title": "Hábitos que Transforman",
                    "author": "María Fernández",
                    "price": 16.99,
                    "originalPrice": 21.99,
                    "rating": 4.9,
                    "reviewCount": 203,
                    "cover": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
                    "description": "Una guía práctica para crear hábitos positivos que te llevarán al éxito en todas las áreas de tu vida.",
                    "category": "Productividad",
                    "pages": 312,
                    "bestseller": False,
                    "fileUrl": "https://example.com/books/habitos-transforman.pdf"
                },
                {
                    "title": "Supera tus Miedos",
                    "author": "María Fernández",
                    "price": 22.99,
                    "originalPrice": 27.99,
                    "rating": 4.7,
                    "reviewCount": 89,
                    "cover": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1228&q=80",
                    "description": "Aprende técnicas probadas para vencer tus miedos y limitaciones, y alcanzar tu máximo potencial.",
                    "category": "Crecimiento Personal",
                    "pages": 198,
                    "bestseller": True,
                    "fileUrl": "https://example.com/books/supera-miedos.pdf"
                },
                {
                    "title": "Liderazgo Auténtico",
                    "author": "María Fernández",
                    "price": 24.99,
                    "originalPrice": 29.99,
                    "rating": 4.9,
                    "reviewCount": 134,
                    "cover": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
                    "description": "Desarrolla tu capacidad de liderazgo auténtico y aprende a inspirar y motivar a otros hacia el éxito.",
                    "category": "Liderazgo",
                    "pages": 278,
                    "bestseller": False,
                    "fileUrl": "https://example.com/books/liderazgo-autentico.pdf"
                }
            ]
            await db.books.insert_many(sample_books)
            logger.info(f"Inserted {len(sample_books)} sample books")
        
        # Initialize Reviews
        reviews_count = await db.reviews.count_documents({})
        if reviews_count == 0:
            sample_reviews = [
                {
                    "author": "Carlos Mendoza",
                    "title": "Escritor y Coach Personal",
                    "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80",
                    "review": "María tiene una habilidad única para transformar conceptos complejos en acciones prácticas. Sus libros son una guía invaluable para cualquier persona que busque crecimiento personal.",
                    "rating": 5,
                    "bookTitle": "El Poder de la Mentalidad Positiva",
                    "featured": True
                },
                {
                    "author": "Ana García",
                    "title": "Psicóloga Clínica",
                    "avatar": "https://images.unsplash.com/photo-1494790108755-2616b612b093?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80",
                    "review": "Los libros de María combinan perfectamente la teoría psicológica con ejercicios prácticos. He recomendado sus obras a muchos de mis pacientes con excelentes resultados.",
                    "rating": 5,
                    "bookTitle": "Hábitos que Transforman",
                    "featured": True
                },
                {
                    "author": "Roberto Silva",
                    "title": "CEO de Innovación Empresarial",
                    "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80",
                    "review": "Como líder empresarial, he encontrado en los libros de María herramientas poderosas que he aplicado tanto en mi vida personal como profesional. Altamente recomendado.",
                    "rating": 5,
                    "bookTitle": "Liderazgo Auténtico",
                    "featured": True
                },
                {
                    "author": "Laura Martínez",
                    "title": "Coach de Vida Certificada", 
                    "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80",
                    "review": "María escribe con una claridad y profundidad excepcionales. Sus estrategias para superar miedos han sido transformadoras para mis clientes y para mí misma.",
                    "rating": 5,
                    "bookTitle": "Supera tus Miedos",
                    "featured": True
                }
            ]
            await db.reviews.insert_many(sample_reviews)
            logger.info(f"Inserted {len(sample_reviews)} sample reviews")

        # Initialize Author Info
        author_count = await db.author.count_documents({})
        if author_count == 0:
            sample_author = {
                "name": "María Fernández",
                "title": "Autora de Bestsellers en Desarrollo Personal",
                "bio": "María Fernández es una reconocida autora y coach especializada en desarrollo personal con más de 15 años de experiencia. Ha ayudado a miles de personas a transformar sus vidas a través de sus libros, talleres y programas de mentoring. Sus obras han sido traducidas a múltiples idiomas y han alcanzado las listas de bestsellers internacionales.",
                "avatar": "https://images.unsplash.com/photo-1494790108755-2616b612b093?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
                "achievements": [
                    "Más de 500,000 libros vendidos mundialmente",
                    "Certificada en PNL y Coaching Ontológico",
                    "Conferencista internacional en desarrollo personal", 
                    "Fundadora de la Academia de Transformación Personal"
                ],
                "socialMedia": {
                    "instagram": "@mariafernandezautor",
                    "facebook": "MariaFernandezLibros",
                    "linkedin": "maria-fernandez-autor"
                },
                "stats": {
                    "booksPublished": 12,
                    "readersReached": "500K+",
                    "averageRating": 4.8,
                    "countries": 25
                }
            }
            await db.author.insert_one(sample_author)
            logger.info("Inserted author information")
            
    except Exception as e:
        logger.error(f"Error initializing sample data: {e}")
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
import uuid
import secrets

from models import Order, OrderCreate, OrderStatus, PaymentStatus, DownloadLink
from database import get_database


class OrderService:
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db or get_database()
        self.collection = self.db.orders

    async def create_order(self, order_create: OrderCreate) -> Order:
        """Create a new order"""
        order_data = {
            "orderId": str(uuid.uuid4()),
            "items": [item.model_dump() for item in order_create.items],
            "customer": order_create.customer.model_dump(),
            "paymentInfo": {
                "amount": sum(item.price * item.quantity for item in order_create.items),
                "status": PaymentStatus.PENDING
            },
            "downloadLinks": [],
            "status": OrderStatus.PENDING,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(order_data)
        order_data['_id'] = str(result.inserted_id)
        
        return Order(**order_data)

    async def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by orderId (not MongoDB _id)"""
        order_data = await self.collection.find_one({"orderId": order_id})
        
        if order_data:
            order_data['_id'] = str(order_data['_id'])
            return Order(**order_data)
        
        return None

    async def get_order_by_mongodb_id(self, mongodb_id: str) -> Optional[Order]:
        """Get order by MongoDB _id"""
        if not ObjectId.is_valid(mongodb_id):
            return None
            
        order_data = await self.collection.find_one({"_id": ObjectId(mongodb_id)})
        
        if order_data:
            order_data['_id'] = str(order_data['_id'])
            return Order(**order_data)
        
        return None

    async def get_orders_by_email(self, email: str) -> List[Order]:
        """Get all orders for a customer by email"""
        cursor = self.collection.find({"customer.email": email})
        orders_data = await cursor.to_list(length=None)
        
        orders = []
        for order_data in orders_data:
            order_data['_id'] = str(order_data['_id'])
            orders.append(Order(**order_data))
        
        return orders

    async def update_order_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        """Update order status"""
        update_data = {
            "status": status,
            "updatedAt": datetime.utcnow()
        }
        
        result = await self.collection.find_one_and_update(
            {"orderId": order_id},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            result['_id'] = str(result['_id'])
            return Order(**result)
        
        return None

    async def update_payment_info(self, order_id: str, payment_intent_id: str, status: PaymentStatus) -> Optional[Order]:
        """Update payment information"""
        update_data = {
            "paymentInfo.paymentIntentId": payment_intent_id,
            "paymentInfo.status": status,
            "updatedAt": datetime.utcnow()
        }
        
        result = await self.collection.find_one_and_update(
            {"orderId": order_id},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            result['_id'] = str(result['_id'])
            return Order(**result)
        
        return None

    async def generate_download_links(self, order_id: str) -> Optional[Order]:
        """Generate secure download links for purchased books"""
        order = await self.get_order_by_id(order_id)
        if not order or order.paymentInfo.status != PaymentStatus.COMPLETED:
            return None

        # Generate download links for each book
        download_links = []
        for item in order.items:
            # Generate secure download token
            download_token = secrets.token_urlsafe(32)
            # Links expire in 48 hours
            expires_at = datetime.utcnow() + timedelta(hours=48)
            
            download_link = DownloadLink(
                bookId=item.bookId,
                bookTitle=item.title,
                downloadUrl=f"/api/download/{download_token}",
                expiresAt=expires_at
            )
            download_links.append(download_link)

        # Update order with download links
        update_data = {
            "downloadLinks": [link.model_dump() for link in download_links],
            "status": OrderStatus.DELIVERED,
            "updatedAt": datetime.utcnow()
        }
        
        result = await self.collection.find_one_and_update(
            {"orderId": order_id},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            result['_id'] = str(result['_id'])
            return Order(**result)
        
        return None

    async def get_order_stats(self) -> dict:
        """Get order statistics"""
        total_orders = await self.collection.count_documents({})
        completed_orders = await self.collection.count_documents({"status": OrderStatus.DELIVERED})
        pending_orders = await self.collection.count_documents({"status": OrderStatus.PENDING})
        
        # Calculate total revenue
        pipeline = [
            {"$match": {"status": OrderStatus.DELIVERED}},
            {
                "$group": {
                    "_id": None,
                    "totalRevenue": {"$sum": "$paymentInfo.amount"}
                }
            }
        ]
        
        cursor = self.collection.aggregate(pipeline)
        revenue_stats = await cursor.to_list(length=1)
        
        total_revenue = revenue_stats[0]['totalRevenue'] if revenue_stats else 0
        
        return {
            "totalOrders": total_orders,
            "completedOrders": completed_orders,
            "pendingOrders": pending_orders,
            "totalRevenue": round(total_revenue, 2)
        }

    async def get_recent_orders(self, limit: int = 10) -> List[Order]:
        """Get recent orders"""
        cursor = self.collection.find({}).sort("createdAt", -1).limit(limit)
        orders_data = await cursor.to_list(length=limit)
        
        orders = []
        for order_data in orders_data:
            order_data['_id'] = str(order_data['_id'])
            orders.append(Order(**order_data))
        
        return orders
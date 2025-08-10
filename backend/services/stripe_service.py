import os
import stripe
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_dummy_key")

class StripeService:
    def __init__(self):
        self.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_dummy_key")
        if self.api_key == "sk_test_dummy_key":
            logger.warning("Using dummy Stripe key - payments will not work in production")

    async def create_payment_intent(self, amount: float, order_id: str, customer_email: str) -> dict:
        """Create a Stripe PaymentIntent"""
        try:
            # Convert amount to cents (Stripe uses cents)
            amount_cents = int(amount * 100)
            
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                metadata={
                    'order_id': order_id,
                    'customer_email': customer_email
                },
                receipt_email=customer_email,
                description=f"Compra de ebooks - Orden #{order_id}"
            )
            
            return {
                "success": True,
                "clientSecret": payment_intent.client_secret,
                "paymentIntentId": payment_intent.id,
                "amount": amount
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating payment intent: {e}")
            return {
                "success": False,
                "error": str(e),
                "clientSecret": None,
                "paymentIntentId": None
            }
        except Exception as e:
            logger.error(f"Unexpected error creating payment intent: {e}")
            return {
                "success": False,
                "error": "Error interno del servidor",
                "clientSecret": None,
                "paymentIntentId": None
            }

    async def confirm_payment(self, payment_intent_id: str) -> dict:
        """Confirm payment status with Stripe"""
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                "success": True,
                "status": payment_intent.status,
                "amount": payment_intent.amount / 100,  # Convert from cents
                "metadata": payment_intent.metadata
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error confirming payment: {e}")
            return {
                "success": False,
                "error": str(e),
                "status": None
            }
        except Exception as e:
            logger.error(f"Unexpected error confirming payment: {e}")
            return {
                "success": False,
                "error": "Error interno del servidor",
                "status": None
            }

    async def create_customer(self, email: str, name: str) -> Optional[dict]:
        """Create a Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                description=f"Cliente de ebooks: {name}"
            )
            
            return {
                "success": True,
                "customer_id": customer.id,
                "email": customer.email
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating customer: {e}")
            return {
                "success": False,
                "error": str(e),
                "customer_id": None
            }

    async def handle_webhook(self, payload: str, signature: str) -> dict:
        """Handle Stripe webhook"""
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        
        if not webhook_secret:
            logger.warning("No webhook secret configured")
            return {"success": False, "error": "Webhook secret not configured"}
        
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            # Handle the event
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                order_id = payment_intent.get('metadata', {}).get('order_id')
                
                return {
                    "success": True,
                    "event_type": "payment_succeeded",
                    "order_id": order_id,
                    "payment_intent_id": payment_intent['id'],
                    "amount": payment_intent['amount'] / 100
                }
                
            elif event['type'] == 'payment_intent.payment_failed':
                payment_intent = event['data']['object']
                order_id = payment_intent.get('metadata', {}).get('order_id')
                
                return {
                    "success": True,
                    "event_type": "payment_failed",
                    "order_id": order_id,
                    "payment_intent_id": payment_intent['id'],
                    "error": payment_intent.get('last_payment_error', {}).get('message', 'Unknown error')
                }
            
            else:
                return {
                    "success": True,
                    "event_type": "unhandled",
                    "message": f"Unhandled event type: {event['type']}"
                }
                
        except ValueError as e:
            logger.error(f"Invalid payload: {e}")
            return {"success": False, "error": "Invalid payload"}
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {e}")
            return {"success": False, "error": "Invalid signature"}
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return {"success": False, "error": str(e)}

    def get_publishable_key(self) -> str:
        """Get Stripe publishable key for frontend"""
        return os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_dummy_key")
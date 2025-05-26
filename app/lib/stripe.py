import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY

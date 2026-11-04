from fastapi import APIRouter

from app.api.routes import private, utils
from app.core.config import settings
from app.modules.admin.routes import router as admin_router
from app.modules.auth.routes import router as auth_router
from app.modules.users.routes import router as users_router
from app.modules.vendors.routes import router as vendors_router
from app.modules.products.routes import router as products_router
from app.modules.stays.routes import router as stays_router
from app.modules.orders.routes import router as orders_router
from app.modules.bookings.routes import router as bookings_router
from app.modules.reviews.routes import router as reviews_router
from app.modules.conversations.routes import router as conversations_router
from app.modules.wishlist.routes import router as wishlist_router
from app.modules.payments.routes import router as payments_router
from app.modules.guides.routes import router as guides_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(vendors_router)
api_router.include_router(products_router)
api_router.include_router(stays_router)
api_router.include_router(orders_router)
api_router.include_router(bookings_router)
api_router.include_router(reviews_router)
api_router.include_router(conversations_router)
api_router.include_router(wishlist_router)
api_router.include_router(payments_router)
api_router.include_router(guides_router)
api_router.include_router(admin_router)
api_router.include_router(utils.router)

if settings.ENVIRONMENT == 'local':
    api_router.include_router(private.router)

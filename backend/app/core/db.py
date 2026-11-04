from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.modules.users.models import User, UserRole
from app.modules.users.schemas import UserCreate
from app.modules.vendors.models import VendorProfile  # noqa: F401
from app.modules.products.models import Product  # noqa: F401
from app.modules.stays.models import Stay  # noqa: F401
from app.modules.orders.models import Order, OrderItem  # noqa: F401
from app.modules.bookings.models import Booking  # noqa: F401
from app.modules.reviews.models import Review  # noqa: F401
from app.modules.conversations.models import Conversation, Message  # noqa: F401
from app.modules.wishlist.models import WishlistItem  # noqa: F401
from app.modules.payments.models import PaymentTransaction  # noqa: F401
from app.modules.admin.models import AuditLog  # noqa: F401
from app.modules.guides.models import Guide  # noqa: F401

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    from app.modules.users.service import create_user

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            role=UserRole.ADMIN,
        )
        user = create_user(session=session, user_create=user_in)
    elif user.role != UserRole.ADMIN:
        user.role = UserRole.ADMIN
        session.add(user)
        session.commit()

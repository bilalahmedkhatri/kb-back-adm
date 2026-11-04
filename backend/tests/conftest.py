from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.modules.admin.models import AuditLog
from app.modules.bookings.models import Booking
from app.modules.conversations.models import Conversation, Message
from app.modules.orders.models import Order, OrderItem
from app.modules.payments.models import PaymentTransaction
from app.modules.products.models import Product
from app.modules.reviews.models import Review
from app.modules.stays.models import Stay
from app.modules.users.models import User
from app.modules.vendors.models import VendorProfile
from app.modules.wishlist.models import WishlistItem
from app.modules.guides.models import Guide
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session]:
    with Session(engine) as session:
        init_db(session)
        yield session
        session.execute(delete(Guide))
        session.execute(delete(PaymentTransaction))
        session.execute(delete(WishlistItem))
        session.execute(delete(AuditLog))
        session.execute(delete(Message))
        session.execute(delete(Conversation))
        session.execute(delete(Review))
        session.execute(delete(Booking))
        session.execute(delete(OrderItem))
        session.execute(delete(Order))
        session.execute(delete(Product))
        session.execute(delete(Stay))
        session.execute(delete(VendorProfile))
        session.execute(delete(User))
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )

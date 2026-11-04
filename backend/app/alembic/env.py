import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

config = context.config

assert config.config_file_name is not None
fileConfig(config.config_file_name)

from sqlmodel import SQLModel  # noqa

from app.core.config import settings  # noqa
from app.modules.auth.models import Message, NewPassword, Token, TokenPayload  # noqa: F401
from app.modules.users.models import User  # noqa: F401
from app.modules.vendors.models import VendorProfile  # noqa: F401
from app.modules.products.models import Product  # noqa: F401
from app.modules.stays.models import Stay  # noqa: F401
from app.modules.orders.models import Order, OrderItem  # noqa: F401
from app.modules.bookings.models import Booking  # noqa: F401
from app.modules.reviews.models import Review  # noqa: F401
from app.modules.conversations.models import Conversation, Message as ConversationMessage  # noqa: F401
from app.modules.wishlist.models import WishlistItem  # noqa: F401
from app.modules.payments.models import PaymentTransaction  # noqa: F401
from app.modules.admin.models import AuditLog  # noqa: F401
from app.modules.guides.models import Guide  # noqa: F401

target_metadata = SQLModel.metadata


def get_url():
    return str(getattr(settings, "SQLALCHEMY_DATABASE_URI_UNPOOLED", settings.SQLALCHEMY_DATABASE_URI))


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    assert configuration is not None
    configuration['sqlalchemy.url'] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

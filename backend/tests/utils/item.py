from sqlmodel import Session

from app.modules.products.models import Product
from app.modules.products.schemas import ProductCreate
from app.modules.products.service import create_product
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string


def create_random_product(db: Session) -> Product:
    user = create_random_user(db)
    vendor_id = user.id
    assert vendor_id is not None
    name = random_lower_string()
    description = random_lower_string()
    product_in = ProductCreate(
        name=name,
        description=description,
        price=10.0,
        currency="AUD",
        category="General",
        origin_island="Tarawa",
        stock=5,
    )
    return create_product(session=db, product_in=product_in, vendor_id=vendor_id)

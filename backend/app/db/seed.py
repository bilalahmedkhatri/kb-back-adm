import uuid
from datetime import UTC, datetime, timedelta
from sqlmodel import Session, select

from app.core.db import engine
from app.core.security import get_password_hash
from app.modules.users.models import User, UserRole
from app.modules.vendors.models import VendorProfile
from app.modules.products.models import Product
from app.modules.stays.models import Stay
from app.modules.orders.models import Order, OrderItem
from app.modules.bookings.models import Booking
from app.modules.reviews.models import Review
from app.modules.conversations.models import Conversation, Message
from app.modules.wishlist.models import WishlistItem
from app.modules.payments.models import PaymentTransaction
from app.modules.admin.models import AuditLog
from app.modules.guides.models import Guide


def seed_database():
    print("=========================================")
    print("     COMPREHENSIVE DATABASE SEEDING      ")
    print("=========================================")

    with Session(engine) as session:
        # 1. Seed 1 Admin User
        admin = session.exec(select(User).where(User.email == "admin@kiribati.ki")).first()
        if not admin:
            admin = User(
                email="admin@kiribati.ki",
                full_name="Kiribati Platform Admin",
                phone="+686 730 0000",
                whatsapp="+686 730 0000",
                avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb",
                hashed_password=get_password_hash("password123"),
                role=UserRole.ADMIN,
                is_superuser=True,
                is_active=True,
            )
            session.add(admin)
            session.commit()
            session.refresh(admin)

            audit1 = AuditLog(
                user_id=admin.id,
                action="VENDOR_VERIFY",
                resource_type="vendor",
                resource_id="maria@tebwa.shop",
                details={"status": "verified", "reason": "Documents approved"},
            )
            session.add(audit1)
            session.commit()
            print(" [+] Created Admin Account & Audit Logs")

        # 2. Seed 3 Vendors
        vendors_info = [
            {
                "email": "maria@tebwa.shop",
                "full_name": "Maria Tebwa",
                "phone": "+686 730 1101",
                "whatsapp": "+686 730 1101",
                "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2",
                "business_name": "Tebwa Shell Handicrafts",
                "bio": "Master artisan specializing in traditional Kiribati seashell jewelry & coconut crafts.",
                "address": "Bikenibeu, South Tarawa, Kiribati",
            },
            {
                "email": "tione@karanga.art",
                "full_name": "Tione Karanga",
                "phone": "+686 730 2202",
                "whatsapp": "+686 730 2202",
                "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d",
                "business_name": "Karanga Traditional Wood Carvings",
                "bio": "Wood carving master with over 20 years experience crafting sacred maneaba sculptures.",
                "address": "London, Kiritimati Island, Kiribati",
            },
            {
                "email": "nei@reraweaves.fi",
                "full_name": "Nei Reraweaves",
                "phone": "+686 730 3303",
                "whatsapp": "+686 730 3303",
                "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2",
                "business_name": "Nei Rera Island Weaving Collective",
                "bio": "Pandanus weaving collective producing authentic Kiribati bags, wall hangings and placemats.",
                "address": "Tebunginako, Abaiang, Kiribati",
            },
        ]

        vendors_dict = {}
        for v in vendors_info:
            usr = session.exec(select(User).where(User.email == v["email"])).first()
            if not usr:
                usr = User(
                    email=v["email"],
                    full_name=v["full_name"],
                    phone=v["phone"],
                    whatsapp=v["whatsapp"],
                    avatar_url=v["avatar"],
                    hashed_password=get_password_hash("password123"),
                    role=UserRole.VENDOR,
                    is_active=True,
                )
                session.add(usr)
                session.commit()
                session.refresh(usr)

            prof = session.exec(select(VendorProfile).where(VendorProfile.user_id == usr.id)).first()
            if not prof:
                prof = VendorProfile(
                    user_id=usr.id,
                    business_name=v["business_name"],
                    business_description=v["bio"],
                    contact_phone=v["phone"],
                    business_address=v["address"],
                    verification_status="verified",
                )
                session.add(prof)
                session.commit()

            vendors_dict[v["email"]] = usr
            print(f" [+] Verified Vendor Profile: {v['full_name']} ({v['email']})")

        # 3. Seed Products (3 Products per Vendor = 9 Total)
        products_catalog = [
            # Maria's Products
            {
                "name": "Tebwa Shell Necklace",
                "description": "Handcrafted necklace made from polished coconut shell and local Kiribati seashells.",
                "price": 45.0,
                "category": "Jewelry",
                "origin_island": "Tarawa",
                "material": "Coconut shell, seashells",
                "stock": 15,
                "vendor_email": "maria@tebwa.shop",
                "images": ["https://picsum.photos/seed/prod1a/400/400"],
            },
            {
                "name": "Tropical Fish Earrings",
                "description": "Playful earrings shaped like tropical reef fish, made from resin and tiny seashells.",
                "price": 28.0,
                "category": "Jewelry",
                "origin_island": "Tarawa",
                "material": "Resin, shells, silver hooks",
                "stock": 25,
                "vendor_email": "maria@tebwa.shop",
                "images": ["https://picsum.photos/seed/prod6a/400/400"],
            },
            {
                "name": "Shell Wind Chime",
                "description": "Melodious wind chime made from assorted seashells collected from Tarawa's pristine beaches.",
                "price": 35.0,
                "category": "Homewares",
                "origin_island": "Tarawa",
                "material": "Seashells, coconut fiber",
                "stock": 20,
                "vendor_email": "maria@tebwa.shop",
                "images": ["https://picsum.photos/seed/prod4a/400/400"],
            },
            # Tione's Products
            {
                "name": "Maneaba Spirit Carving",
                "description": "Intricate wood carving depicting the spirit of the maneaba (community meeting house).",
                "price": 120.0,
                "category": "Carvings",
                "origin_island": "Kiritimati",
                "material": "Te tea wood",
                "stock": 5,
                "vendor_email": "tione@karanga.art",
                "images": ["https://picsum.photos/seed/prod3a/400/400"],
            },
            {
                "name": "Frigatebird Sculpture",
                "description": "Sculpture of the magnificent frigatebird, Kiribati's national bird, carved in mid-flight.",
                "price": 150.0,
                "category": "Carvings",
                "origin_island": "Kiritimati",
                "material": "Ironwood",
                "stock": 4,
                "vendor_email": "tione@karanga.art",
                "images": ["https://picsum.photos/seed/prod12a/400/400"],
            },
            {
                "name": "Miniature Outrigger Canoe",
                "description": "Detailed miniature replica of a traditional Kiribati outrigger sailing canoe.",
                "price": 85.0,
                "category": "Carvings",
                "origin_island": "Kiritimati",
                "material": "Te tea wood, fiber",
                "stock": 6,
                "vendor_email": "tione@karanga.art",
                "images": ["https://picsum.photos/seed/prod19a/400/400"],
            },
            # Nei Rera's Products
            {
                "name": "Pandanus Weave Bag",
                "description": "Traditional pandanus leaf woven bag, perfect for beach days or market shopping.",
                "price": 65.0,
                "category": "Textiles",
                "origin_island": "Abaiang",
                "material": "Pandanus leaves",
                "stock": 10,
                "vendor_email": "nei@reraweaves.fi",
                "images": ["https://picsum.photos/seed/prod2a/400/400"],
            },
            {
                "name": "Pandanus Wall Hanging",
                "description": "Large decorative wall hanging woven from dyed pandanus strips in traditional patterns.",
                "price": 90.0,
                "category": "Textiles",
                "origin_island": "Abaiang",
                "material": "Pandanus, natural plant dyes",
                "stock": 7,
                "vendor_email": "nei@reraweaves.fi",
                "images": ["https://picsum.photos/seed/prod8a/400/400"],
            },
            {
                "name": "Tablet Weave Placemats Set",
                "description": "Set of 4 handwoven pandanus placemats in natural earth tones.",
                "price": 40.0,
                "category": "Textiles",
                "origin_island": "Abaiang",
                "material": "Pandanus leaves",
                "stock": 18,
                "vendor_email": "nei@reraweaves.fi",
                "images": ["https://picsum.photos/seed/prod13a/400/400"],
            },
        ]

        seeded_products = []
        for p in products_catalog:
            vendor = vendors_dict[p["vendor_email"]]
            prod = session.exec(select(Product).where(Product.name == p["name"])).first()
            if not prod:
                prod = Product(
                    name=p["name"],
                    description=p["description"],
                    price=p["price"],
                    currency="AUD",
                    category=p["category"],
                    origin_island=p["origin_island"],
                    material=p["material"],
                    stock=p["stock"],
                    status="active",
                    images=p["images"],
                    vendor_id=vendor.id,
                )
                session.add(prod)
                session.commit()
                session.refresh(prod)
            seeded_products.append(prod)
            print(f" [+] Seeded Product: {p['name']} (${p['price']} AUD)")

        # 4. Seed Stays (2 Stays per Vendor = 6 Total)
        stays_catalog = [
            # Maria's Stays
            {
                "name": "Tebwa Beachfront Homestay",
                "description": "Authentic Kiribati beachfront homestay with traditional breakfast and ocean views.",
                "price_per_night": 85.0,
                "type": "homestay",
                "location": "Bikenibeu",
                "island": "Tarawa",
                "max_guests": 4,
                "bedrooms": 2,
                "beds": 3,
                "bathrooms": 1,
                "amenities": ["WiFi", "Breakfast", "Beach access", "Kayak"],
                "host_email": "maria@tebwa.shop",
                "images": ["https://picsum.photos/seed/stay1/600/400"],
            },
            {
                "name": "Tarawa Oceanview Villa",
                "description": "Spacious villa with panoramic ocean views, private beach access, and full kitchen.",
                "price_per_night": 200.0,
                "type": "villa",
                "location": "Bairiki",
                "island": "Tarawa",
                "max_guests": 8,
                "bedrooms": 4,
                "beds": 5,
                "bathrooms": 3,
                "amenities": ["WiFi", "Full kitchen", "Aircon", "Private beach"],
                "host_email": "maria@tebwa.shop",
                "images": ["https://picsum.photos/seed/stay3/600/400"],
            },
            # Tione's Stays
            {
                "name": "Eco Lagoon Retreat",
                "description": "Sustainable eco-lodge among coconut palms with direct lagoon access and snorkeling.",
                "price_per_night": 150.0,
                "type": "eco-lodge",
                "location": "London",
                "island": "Kiritimati",
                "max_guests": 6,
                "bedrooms": 3,
                "beds": 4,
                "bathrooms": 2,
                "amenities": ["WiFi", "Restaurant", "Snorkeling gear", "Bike rental"],
                "host_email": "tione@karanga.art",
                "images": ["https://picsum.photos/seed/stay2/600/400"],
            },
            {
                "name": "Palm Grove Guesthouse",
                "description": "Cozy guesthouse surrounded by coconut palms - perfect base for exploring Kiritimati.",
                "price_per_night": 60.0,
                "type": "guesthouse",
                "location": "Tabwakea",
                "island": "Kiritimati",
                "max_guests": 3,
                "bedrooms": 1,
                "beds": 2,
                "bathrooms": 1,
                "amenities": ["WiFi", "Breakfast", "Garden", "Bicycle"],
                "host_email": "tione@karanga.art",
                "images": ["https://picsum.photos/seed/stay4/600/400"],
            },
            # Nei Rera's Stays
            {
                "name": "Abaiang Bird Sanctuary Lodge",
                "description": "Remote eco-lodge on a pristine island sanctuary - paradise for nature lovers.",
                "price_per_night": 130.0,
                "type": "eco-lodge",
                "location": "Tebunginako",
                "island": "Abaiang",
                "max_guests": 4,
                "bedrooms": 2,
                "beds": 2,
                "bathrooms": 1,
                "amenities": ["Bird watching", "Hiking", "Solar power", "Meals included"],
                "host_email": "nei@reraweaves.fi",
                "images": ["https://picsum.photos/seed/stay9/600/400"],
            },
            {
                "name": "Lagoon Breeze Homestay",
                "description": "Charming island homestay with access to spectacular lagoon tide pools.",
                "price_per_night": 55.0,
                "type": "homestay",
                "location": "Buota",
                "island": "Abaiang",
                "max_guests": 2,
                "bedrooms": 1,
                "beds": 1,
                "bathrooms": 1,
                "amenities": ["Breakfast", "Tide pool access", "Fishing guide"],
                "host_email": "nei@reraweaves.fi",
                "images": ["https://picsum.photos/seed/stay11/600/400"],
            },
        ]

        seeded_stays = []
        for s in stays_catalog:
            host = vendors_dict[s["host_email"]]
            stay = session.exec(select(Stay).where(Stay.name == s["name"])).first()
            if not stay:
                stay = Stay(
                    name=s["name"],
                    description=s["description"],
                    price_per_night=s["price_per_night"],
                    currency="AUD",
                    type=s["type"],
                    location=s["location"],
                    island=s["island"],
                    max_guests=s["max_guests"],
                    bedrooms=s["bedrooms"],
                    beds=s["beds"],
                    bathrooms=s["bathrooms"],
                    amenities=s["amenities"],
                    eco_credentials={"solar_power": True, "rainwater_collection": True, "coral_reef_protection": True},
                    languages_spoken=["English", "Kiribati (Gilbertese)"],
                    status="active",
                    images=s["images"],
                    host_id=host.id,
                )
                session.add(stay)
                session.commit()
                session.refresh(stay)
            else:
                if not stay.languages_spoken:
                    stay.languages_spoken = ["English", "Kiribati (Gilbertese)"]
                if not stay.eco_credentials:
                    stay.eco_credentials = {"solar_power": True, "rainwater_collection": True, "coral_reef_protection": True}
                session.add(stay)
                session.commit()
                session.refresh(stay)
            seeded_stays.append(stay)
            print(f" [+] Seeded Stay: {s['name']} (${s['price_per_night']} AUD/night)")

        # 5. Seed 3 Customers
        customers_info = [
            {
                "email": "john@example.com",
                "full_name": "John Smith",
                "phone": "+61 400 111 222",
                "whatsapp": "+61 400 111 222",
                "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e",
                "address": {"fullName": "John Smith", "street": "42 Ocean Parade", "city": "Sydney", "state": "NSW", "zip": "2000", "country": "Australia", "phone": "+61 400 111 222"},
            },
            {
                "email": "sarah@example.com",
                "full_name": "Sarah Jones",
                "phone": "+61 400 333 444",
                "whatsapp": "+61 400 333 444",
                "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330",
                "address": {"fullName": "Sarah Jones", "street": "88 Beachfront Ave", "city": "Melbourne", "state": "VIC", "zip": "3000", "country": "Australia", "phone": "+61 400 333 444"},
            },
            {
                "email": "mike@example.com",
                "full_name": "Mike Chen",
                "phone": "+1 415 555 0199",
                "whatsapp": "+1 415 555 0199",
                "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e",
                "address": {"fullName": "Mike Chen", "street": "500 Market St", "city": "San Francisco", "state": "CA", "zip": "94105", "country": "USA", "phone": "+1 415 555 0199"},
            },
        ]

        customers_list = []
        for c in customers_info:
            usr = session.exec(select(User).where(User.email == c["email"])).first()
            if not usr:
                usr = User(
                    email=c["email"],
                    full_name=c["full_name"],
                    phone=c["phone"],
                    whatsapp=c["whatsapp"],
                    avatar_url=c["avatar"],
                    hashed_password=get_password_hash("password123"),
                    role=UserRole.CUSTOMER,
                    is_active=True,
                )
                session.add(usr)
                session.commit()
                session.refresh(usr)
            customers_list.append((usr, c["address"]))
            print(f" [+] Seeded Customer Profile: {c['full_name']} ({c['email']})")

        # 6. Seed 3 Orders, 3 Stay Bookings, 2 Confirmed Reviews, 3 Conversations, Wishlist & Payments per Customer!
        statuses = ["delivered", "shipped", "pending"]
        b_statuses = ["confirmed", "confirmed", "cancelled"]

        for idx, (cust, addr) in enumerate(customers_list):
            print(f"\n --- Seeding User Data for: {cust.full_name} ---")

            # A. 3 Orders per Customer
            for o_idx in range(3):
                p1 = seeded_products[(idx * 3 + o_idx) % len(seeded_products)]
                p2 = seeded_products[(idx * 3 + o_idx + 1) % len(seeded_products)]

                subtotal = p1.price + p2.price
                delivery_fee = 15.0
                total = subtotal + delivery_fee
                status = statuses[o_idx]

                ord_obj = Order(
                    user_id=cust.id,
                    subtotal=subtotal,
                    delivery_fee=delivery_fee,
                    tax=0.0,
                    total=total,
                    currency="AUD",
                    status=status,
                    shipping_address=addr,
                    tracking_number=f"KB-TRK-{cust.id.hex[:4]}-{o_idx+100}",
                )
                session.add(ord_obj)
                session.commit()
                session.refresh(ord_obj)

                i1 = OrderItem(order_id=ord_obj.id, product_id=p1.id, name=p1.name, price=p1.price, quantity=1, image=p1.images[0])
                i2 = OrderItem(order_id=ord_obj.id, product_id=p2.id, name=p2.name, price=p2.price, quantity=1, image=p2.images[0])
                session.add_all([i1, i2])
                session.commit()

                # Payment Transaction record
                pay_tx = PaymentTransaction(
                    user_id=cust.id,
                    order_id=ord_obj.id,
                    amount=total,
                    currency="AUD",
                    provider="stripe" if o_idx % 2 == 0 else "paypal",
                    status="succeeded",
                    transaction_reference=f"TX-STRIPE-{ord_obj.id.hex[:8].upper()}",
                    payment_method_details={"card_brand": "Visa", "last4": "4242"},
                )
                session.add(pay_tx)
                session.commit()

                print(f"   [+] Order #{o_idx+1}: ${total} AUD ({status})")

            # B. 3 Stay Bookings per Customer
            for b_idx in range(3):
                st = seeded_stays[(idx * 2 + b_idx) % len(seeded_stays)]
                now = datetime.now(UTC)
                check_in = now + timedelta(days=b_idx * 10 + 5)
                check_out = check_in + timedelta(days=4)
                b_status = b_statuses[b_idx]

                bk = Booking(
                    user_id=cust.id,
                    stay_id=st.id,
                    check_in=check_in,
                    check_out=check_out,
                    guest_count=2 + b_idx,
                    status=b_status,
                    message=f"Special request for booking at {st.name}.",
                )
                session.add(bk)
                session.commit()
                print(f"   [+] Booking #{b_idx+1}: {st.name} ({b_status})")

            # C. 2 Confirmed Reviews per Customer
            target_prod = seeded_products[idx * 3]
            target_stay = seeded_stays[idx * 2]

            rev_p = Review(
                target_id=target_prod.id,
                target_type="product",
                user_id=cust.id,
                rating=5,
                reviewer_name=cust.full_name,
                comment=f"Exceptional quality! Handcrafted {target_prod.name} exceeded my expectations.",
            )
            rev_s = Review(
                target_id=target_stay.id,
                target_type="stay",
                user_id=cust.id,
                rating=5,
                reviewer_name=cust.full_name,
                comment=f"Unforgettable island experience at {target_stay.name}! Highly recommended.",
            )
            session.add_all([rev_p, rev_s])
            session.commit()
            print("   [+] 2 Confirmed Reviews added (1 Product, 1 Stay)")

            # D. 3 Chat Conversations per Customer (1 per Vendor)
            for v_idx, (v_email, v_user) in enumerate(vendors_dict.items()):
                conv = Conversation(
                    user_id=cust.id,
                    vendor_id=v_user.id,
                    participant_names=[cust.full_name, v_user.full_name],
                    last_message=f"Thank you for the update on my order!",
                    last_message_time=datetime.now(UTC) - timedelta(hours=v_idx),
                    unread=False,
                )
                session.add(conv)
                session.commit()
                session.refresh(conv)

                m1 = Message(
                    conversation_id=conv.id,
                    sender_id=cust.id,
                    text=f"Mauria {v_user.full_name}! Is shipping available to Australia?",
                    timestamp=datetime.now(UTC) - timedelta(hours=v_idx + 2),
                )
                m2 = Message(
                    conversation_id=conv.id,
                    sender_id=v_user.id,
                    text=f"Mauria {cust.full_name}! Yes, we ship internationally with tracking.",
                    timestamp=datetime.now(UTC) - timedelta(hours=v_idx + 1),
                )
                session.add_all([m1, m2])
                session.commit()
            print("   [+] 3 Vendor Chat Conversations created")

            # E. Wishlist Items per Customer
            w1 = WishlistItem(user_id=cust.id, target_id=seeded_products[idx].id, target_type="product")
            w2 = WishlistItem(user_id=cust.id, target_id=seeded_stays[idx].id, target_type="stay")
            session.add_all([w1, w2])
            session.commit()
            print("   [+] Wishlist items saved")

        # 7. Seed Tourism Editorial Guides
        guides_data = [
            {
                "title": "Understanding Kiribati Maneaba Culture & Customs",
                "slug": "understanding-kiribati-maneaba-culture",
                "excerpt": "Discover the central pillar of Kiribati community life - the maneaba meeting house and local etiquette.",
                "content": "The Maneaba is the spiritual and cultural heart of Kiribati community life. Every village has its own maneaba where elders gather...",
                "image": "https://picsum.photos/seed/guide1/800/500",
                "topic": "Culture & Heritage",
                "read_time": 6,
                "featured": True,
            },
            {
                "title": "Kiritimati Island: World Class Bonefishing & Eco Adventures",
                "slug": "kiritimati-island-travel-guide",
                "excerpt": "Explore Christmas Island, the largest coral atoll in the world, renowned for bird watching and pristine flats.",
                "content": "Kiritimati Island offers unparalleled natural beauty and world-renowned flats for fly fishing and marine wildlife exploration...",
                "image": "https://picsum.photos/seed/guide2/800/500",
                "topic": "Travel & Nature",
                "read_time": 8,
                "featured": True,
            },
            {
                "title": "The Ancient Art of Kiribati Pandanus Leaf Weaving",
                "slug": "art-of-pandanus-weaving",
                "excerpt": "Learn how Kiribati master weavers transform raw pandanus leaves into durable bags, mats and ceremonial attire.",
                "content": "Pandanus leaf weaving is a cherished traditional craft passed down through generations of Kiribati women...",
                "image": "https://picsum.photos/seed/guide3/800/500",
                "topic": "Artisan Crafts",
                "read_time": 5,
                "featured": False,
            },
        ]

        for g in guides_data:
            g_obj = session.exec(select(Guide).where(Guide.slug == g["slug"])).first()
            if not g_obj:
                g_obj = Guide(
                    title=g["title"],
                    slug=g["slug"],
                    excerpt=g["excerpt"],
                    content=g["content"],
                    image=g["image"],
                    topic=g["topic"],
                    author_id=admin.id,
                    author_name=admin.full_name,
                    read_time=g["read_time"],
                    featured=g["featured"],
                )
                session.add(g_obj)
                session.commit()
                print(f" [+] Seeded Editorial Guide: {g['title']}")

    print("\n=========================================")
    print(" COMPREHENSIVE SEEDING COMPLETED CLEANLY ")
    print("=========================================")


if __name__ == "__main__":
    seed_database()

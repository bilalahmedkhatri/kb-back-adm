import logging
import uuid
from datetime import UTC, datetime, timedelta
from sqlmodel import Session, select
from app.core.security import get_password_hash
from app.modules.users.models import User, UserRole
from app.modules.products.models import Product
from app.modules.stays.models import Stay
from app.modules.orders.models import Order, OrderItem
from app.modules.bookings.models import Booking
from app.modules.reviews.models import Review
from app.modules.conversations.models import Conversation, Message

logger = logging.getLogger(__name__)

def seed_all(session: Session) -> None:
    logger.info("Seeding realistic Kiribati dummy data...")

    # --- 1. USERS ---
    users_data = [
        {"email": "admin@islandconnects.com", "full_name": "Tekea Bio (Platform Admin)", "role": UserRole.ADMIN, "phone": "+686 73001001", "whatsapp": "+686 73001001", "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb"},
        {"email": "vendor.tarawa@islandconnects.com", "full_name": "Kuria Craftswomen Guild", "role": UserRole.VENDOR, "phone": "+686 73002002", "whatsapp": "+686 73002002", "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2"},
        {"email": "vendor.kiritimati@islandconnects.com", "full_name": "Kiritimati Ocean Weavers", "role": UserRole.VENDOR, "phone": "+686 73002003", "whatsapp": "+686 73002003", "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"},
        {"email": "vendor.abemama@islandconnects.com", "full_name": "Abemama Island Carvers", "role": UserRole.VENDOR, "phone": "+686 73002004", "whatsapp": "+686 73002004", "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e"},
        {"email": "vendor.tabiteuea@islandconnects.com", "full_name": "Tabiteuea Organic Oils", "role": UserRole.VENDOR, "phone": "+686 73002005", "whatsapp": "+686 73002005", "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2"},
        {"email": "customer.sarah@example.com", "full_name": "Sarah Jenkins", "role": UserRole.CUSTOMER, "phone": "+61 412 345 678", "whatsapp": "+61 412 345 678", "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330"},
        {"email": "customer.david@example.com", "full_name": "David Miller", "role": UserRole.CUSTOMER, "phone": "+64 21 987 654", "whatsapp": "+64 21 987 654", "avatar_url": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61"},
        {"email": "customer.emi@example.com", "full_name": "Emi Sato", "role": UserRole.CUSTOMER, "phone": "+81 90 1234 5678", "whatsapp": "+81 90 1234 5678", "avatar_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80"},
    ]

    users = {}
    for u in users_data:
        existing = session.exec(select(User).where(User.email == u["email"])).first()
        if not existing:
            user = User(
                email=u["email"],
                full_name=u["full_name"],
                role=u["role"],
                phone=u["phone"],
                whatsapp=u["whatsapp"],
                avatar_url=u["avatar_url"],
                hashed_password=get_password_hash("password123"),
                is_active=True,
                is_superuser=(u["role"] == UserRole.ADMIN)
            )
            session.add(user)
            users[u["email"]] = user
        else:
            users[u["email"]] = existing
    session.commit()

    tarawa_vendor = users["vendor.tarawa@islandconnects.com"]
    kiritimati_vendor = users["vendor.kiritimati@islandconnects.com"]
    abemama_vendor = users["vendor.abemama@islandconnects.com"]
    tabiteuea_vendor = users["vendor.tabiteuea@islandconnects.com"]
    sarah = users["customer.sarah@example.com"]
    david = users["customer.david@example.com"]
    emi = users["customer.emi@example.com"]

    # --- 2. PRODUCTS ---
    products_data = [
        # Woven Goods
        {"name": "Handwoven Pandanus Mat (Te Rau)", "desc": "Traditional Kiribati Pandanus leaf floor mat intricately woven with natural dye patterns.", "price": 120.0, "category": "Woven Goods", "island": "Tarawa", "material": "Pandanus Leaf", "stock": 15, "vendor": tarawa_vendor, "images": ["https://images.unsplash.com/photo-1606744837616-56c9a5c6a6eb"]},
        {"name": "Kiribati Traditional Woven Fan (Te Techi)", "desc": "Handcrafted palm and pandanus fan decorated with woven geometric motifs.", "price": 35.0, "category": "Accessories", "island": "Kiritimati", "material": "Young Coconut Leaf", "stock": 25, "vendor": kiritimati_vendor, "images": ["https://images.unsplash.com/photo-1584917865442-de89df76afd3"]},
        {"name": "Woven Coconut Leaf Basket", "desc": "Sturdy basket woven from coconut fronds, perfect for gathering or market days.", "price": 45.0, "category": "Woven Goods", "island": "Abemama", "material": "Coconut Fronds", "stock": 20, "vendor": abemama_vendor, "images": ["https://images.unsplash.com/photo-1596403063810-664426b3e648"]},
        {"name": "Te Bwa - Fine Woven Mat", "desc": "Extremely fine sleeping mat woven from bleached pandanus leaves, smooth and soft.", "price": 180.0, "category": "Woven Goods", "island": "Tabiteuea", "material": "Fine Pandanus", "stock": 5, "vendor": tabiteuea_vendor, "images": ["https://images.unsplash.com/photo-1581452243615-ce1bbcb6b29f"]},
        {"name": "Woven Storage Box", "desc": "Decorative woven box with lid for storing valuables, colored with vibrant sea dyes.", "price": 55.0, "category": "Woven Goods", "island": "Tarawa", "material": "Pandanus", "stock": 12, "vendor": tarawa_vendor, "images": ["https://images.unsplash.com/photo-1608744158485-61bd93f72df2"]},
        
        # Wellness & Beauty
        {"name": "Pure Virgin Coconut Oil (500ml)", "desc": "Cold-pressed organic coconut oil extracted by local island communities.", "price": 22.0, "category": "Wellness & Beauty", "island": "Tabiteuea", "material": "100% Organic Coconut", "stock": 40, "vendor": tabiteuea_vendor, "images": ["https://images.unsplash.com/photo-1608571423902-eed4a5ad8108"]},
        {"name": "Frangipani Infused Body Oil", "desc": "Coconut oil infused with local Frangipani flowers for a sweet, floral island scent.", "price": 28.0, "category": "Wellness & Beauty", "island": "Tarawa", "material": "Coconut Oil & Frangipani", "stock": 30, "vendor": tarawa_vendor, "images": ["https://images.unsplash.com/photo-1615397323140-1e5b871ed193"]},
        {"name": "Sea Salt Body Scrub", "desc": "Exfoliating scrub made with pure Kiritimati sea salt and nourishing oils.", "price": 18.0, "category": "Wellness & Beauty", "island": "Kiritimati", "material": "Sea Salt & Oils", "stock": 50, "vendor": kiritimati_vendor, "images": ["https://images.unsplash.com/photo-1596755389378-c31d21fd1273"]},
        
        # Woodcarving
        {"name": "Hand-Carved Outrigger Canoe Model (Te Wa)", "desc": "Detailed miniature replica of the traditional Kiribati sailing canoe.", "price": 250.0, "category": "Woodcarving", "island": "Abemama", "material": "Breadfruit Wood", "stock": 5, "vendor": abemama_vendor, "images": ["https://images.unsplash.com/photo-1544551763-46a013bb70d5"]},
        {"name": "Traditional Wooden Maneaba Model", "desc": "Scale model of the traditional Kiribati meeting house (Maneaba).", "price": 320.0, "category": "Woodcarving", "island": "Tarawa", "material": "Coconut Wood", "stock": 2, "vendor": tarawa_vendor, "images": ["https://images.unsplash.com/photo-1596395359194-e0e64f7b607e"]},
        {"name": "Carved Coconut Shell Bowl", "desc": "Smooth, polished bowl made from a mature coconut shell.", "price": 25.0, "category": "Woodcarving", "island": "Tabiteuea", "material": "Coconut Shell", "stock": 35, "vendor": tabiteuea_vendor, "images": ["https://images.unsplash.com/photo-1601004386708-3ab9a89c8942"]},
        
        # Jewelry
        {"name": "Polished Shell & Pearl Necklace (Te Kura)", "desc": "Hand-strung necklace made from Kiritimati lagoon shells and black lip mother-of-pearl.", "price": 65.0, "category": "Jewelry", "island": "Kiritimati", "material": "Mother-of-Pearl Shells", "stock": 18, "vendor": kiritimati_vendor, "images": ["https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f"]},
        {"name": "Cowrie Shell Bracelet", "desc": "Woven cord bracelet adorned with local white cowrie shells.", "price": 20.0, "category": "Jewelry", "island": "Tarawa", "material": "Cowrie Shells & Cord", "stock": 40, "vendor": tarawa_vendor, "images": ["https://images.unsplash.com/photo-1611085583191-a3b181a88401"]},
        {"name": "Shark Tooth Pendant", "desc": "Traditional warrior-style pendant featuring a real, sustainably sourced shark tooth.", "price": 85.0, "category": "Jewelry", "island": "Abemama", "material": "Shark Tooth & Woven Fibre", "stock": 8, "vendor": abemama_vendor, "images": ["https://images.unsplash.com/photo-1565158652615-5858957ba179"]},
        {"name": "Mother of Pearl Earrings", "desc": "Elegant drop earrings carved from luminous mother of pearl.", "price": 45.0, "category": "Jewelry", "island": "Kiritimati", "material": "Mother of Pearl", "stock": 22, "vendor": kiritimati_vendor, "images": ["https://images.unsplash.com/photo-1535632066927-ab7c9ab60908"]},
        {"name": "Red Spondylus Shell Ring", "desc": "Vibrant red shell ring, traditionally a sign of high status.", "price": 110.0, "category": "Jewelry", "island": "Tabiteuea", "material": "Spondylus Shell", "stock": 4, "vendor": tabiteuea_vendor, "images": ["https://images.unsplash.com/photo-1605100804763-247f67b2548e"]}
    ]

    products = []
    if session.exec(select(Product)).first() is None:
        for p in products_data:
            product = Product(
                name=p["name"],
                description=p["desc"],
                price=p["price"],
                currency="AUD",
                category=p["category"],
                origin_island=p["island"],
                material=p["material"],
                stock=p["stock"],
                status="active",
                images=p["images"],
                vendor_id=p["vendor"].id
            )
            session.add(product)
            products.append(product)
        session.commit()
    else:
        products = list(session.exec(select(Product)).all())

    # --- 3. STAYS ---
    stays_data = [
        {"name": "Bikenibeu Sunset Beach Bungalow", "desc": "Traditional eco-bungalow perched on the pristine lagoon shore of South Tarawa.", "price": 140.0, "type": "eco-lodge", "location": "Bikenibeu", "island": "Tarawa", "guests": 3, "beds": 2, "baths": 1, "amenities": ["Free WiFi", "Breakfast Included", "Ocean View", "Kayaks", "Air Conditioning"], "images": ["https://images.unsplash.com/photo-1499793983690-e29da59ef1c2"], "host": tarawa_vendor},
        {"name": "Ambo Lagoon Villa", "desc": "Modern villa overlooking the tranquil Ambo lagoon. Perfect for remote work and relaxation.", "price": 280.0, "type": "villa", "location": "Ambo", "island": "Tarawa", "guests": 6, "beds": 4, "baths": 3, "amenities": ["Fast WiFi", "Full Kitchen", "Pool", "Ocean View", "Air Conditioning"], "images": ["https://images.unsplash.com/photo-1582719508461-905c673771fd"], "host": tarawa_vendor},
        {"name": "Betio Historical Guesthouse", "desc": "Comfortable guesthouse near historic WWII sites on Betio island.", "price": 95.0, "type": "homestay", "location": "Betio", "island": "Tarawa", "guests": 2, "beds": 1, "baths": 1, "amenities": ["Breakfast Included", "Guided Tours", "Air Conditioning"], "images": ["https://images.unsplash.com/photo-1566073771259-6a8506099945"], "host": tarawa_vendor},
        
        {"name": "Kiritimati Lagoon Fly Fishing Lodge", "desc": "World-class fly fisherman lodge offering guided bonefish tours.", "price": 220.0, "type": "villa", "location": "London Village", "island": "Kiritimati", "guests": 4, "beds": 3, "baths": 2, "amenities": ["Boat Tours", "Fishing Gear Storage", "Air Conditioning", "Airport Transfer"], "images": ["https://images.unsplash.com/photo-1571896349842-33c89424de2d"], "host": kiritimati_vendor},
        {"name": "Paris Eco-Retreat", "desc": "Off-grid eco-retreat nestled in the remote ruins of the 'Paris' settlement.", "price": 110.0, "type": "eco-lodge", "location": "Paris", "island": "Kiritimati", "guests": 2, "beds": 1, "baths": 1, "amenities": ["Solar Power", "Composting Toilet", "Lagoon Access", "Bicycles"], "images": ["https://images.unsplash.com/photo-1510798831971-661eb04b3739"], "host": kiritimati_vendor},
        {"name": "Banana Village Beach House", "desc": "Spacious house near the airport, ideal for transit or short stays.", "price": 160.0, "type": "villa", "location": "Banana", "island": "Kiritimati", "guests": 5, "beds": 3, "baths": 2, "amenities": ["Air Conditioning", "WiFi", "Airport Transfer"], "images": ["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4"], "host": kiritimati_vendor},

        {"name": "Abemama Coral Atoll Homestay", "desc": "Experience authentic island life with a local family on Abemama atoll.", "price": 85.0, "type": "homestay", "location": "Tabontebike", "island": "Abemama", "guests": 2, "beds": 1, "baths": 1, "amenities": ["Traditional Meals", "Cultural Tour", "Bicycle Rental"], "images": ["https://images.unsplash.com/photo-1540541338287-41700207dee6"], "host": abemama_vendor},
        {"name": "Stevenson's Lookout", "desc": "Bungalow near the historical residence of Robert Louis Stevenson.", "price": 130.0, "type": "eco-lodge", "location": "Chesterfield", "island": "Abemama", "guests": 3, "beds": 2, "baths": 1, "amenities": ["Ocean View", "Breakfast Included", "Hammocks"], "images": ["https://images.unsplash.com/photo-1499793983690-e29da59ef1c2"], "host": abemama_vendor},
        {"name": "Kariatebike Beachfront Hut", "desc": "Simple, rustic thatched hut right on the white sand beach.", "price": 60.0, "type": "homestay", "location": "Kariatebike", "island": "Abemama", "guests": 2, "beds": 1, "baths": 1, "amenities": ["Beachfront", "Shared Kitchen", "Campfire"], "images": ["https://images.unsplash.com/photo-1507525428034-b723cf961d3e"], "host": abemama_vendor},

        {"name": "Tabiteuea North Explorer's Base", "desc": "Comfortable base for exploring the largest atoll in the Gilbert group.", "price": 100.0, "type": "homestay", "location": "Utiroa", "island": "Tabiteuea", "guests": 4, "beds": 2, "baths": 1, "amenities": ["Meals Included", "Boat Tours", "WiFi"], "images": ["https://images.unsplash.com/photo-1510414842594-a61c69b5ae57"], "host": tabiteuea_vendor},
        {"name": "Tabiang Village Retreat", "desc": "Quiet retreat offering a deep dive into Kiribati traditional culture.", "price": 90.0, "type": "homestay", "location": "Tabiang", "island": "Tabiteuea", "guests": 2, "beds": 1, "baths": 1, "amenities": ["Weaving Lessons", "Traditional Meals"], "images": ["https://images.unsplash.com/photo-1501504905252-473c47e087f8"], "host": tabiteuea_vendor},
        {"name": "South Tabiteuea Eco-Cabin", "desc": "Remote eco-cabin for ultimate seclusion and pristine snorkeling.", "price": 150.0, "type": "eco-lodge", "location": "Buariki", "island": "Tabiteuea", "guests": 2, "beds": 1, "baths": 1, "amenities": ["Snorkeling Gear", "Solar Power", "Ocean View"], "images": ["https://images.unsplash.com/photo-1439066615861-d1af74d74000"], "host": tabiteuea_vendor},
    ]

    stays = []
    if session.exec(select(Stay)).first() is None:
        for s in stays_data:
            stay = Stay(
                name=s["name"],
                description=s["desc"],
                price_per_night=s["price"],
                currency="AUD",
                type=s["type"],
                location=s["location"],
                island=s["island"],
                max_guests=s["guests"],
                bedrooms=max(1, s["beds"] - 1),
                beds=s["beds"],
                bathrooms=s["baths"],
                amenities=s["amenities"],
                status="active",
                images=s["images"],
                host_id=s["host"].id
            )
            session.add(stay)
            stays.append(stay)
        session.commit()
    else:
        stays = list(session.exec(select(Stay)).all())

    # --- 4. ORDERS ---
    if session.exec(select(Order)).first() is None and len(products) >= 5:
        orders_data = [
            (sarah, [products[0], products[1]], "delivered", "IC-TRK-982144", "42 Ocean Drive", "Sydney", "Australia"),
            (david, [products[11]], "shipped", "IC-TRK-771029", "18 Harbour View Rd", "Auckland", "New Zealand"),
            (emi, [products[5], products[6], products[7]], "confirmed", None, "1-1 Chiyoda", "Tokyo", "Japan"),
            (sarah, [products[3]], "pending", None, "42 Ocean Drive", "Sydney", "Australia"),
            (david, [products[8], products[2]], "delivered", "IC-TRK-554433", "18 Harbour View Rd", "Auckland", "New Zealand"),
        ]

        for user, order_prods, status, tracking, street, city, country in orders_data:
            subtotal = sum(p.price for p in order_prods)
            delivery_fee = 25.0
            tax = subtotal * 0.1
            total = subtotal + delivery_fee + tax
            
            order = Order(
                user_id=user.id,
                total=total,
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                tax=tax,
                currency="AUD",
                status=status,
                tracking_number=tracking,
                shipping_address={"street": street, "city": city, "country": country, "postcode": "0000"}
            )
            session.add(order)
            session.commit()
            session.refresh(order)

            for p in order_prods:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=p.id,
                    name=p.name,
                    price=p.price,
                    quantity=1,
                    image=p.images[0] if p.images else None
                )
                session.add(order_item)
        session.commit()

    # --- 5. BOOKINGS ---
    if session.exec(select(Booking)).first() is None and len(stays) >= 6:
        now = datetime.now(UTC)
        bookings_data = [
            (sarah, stays[0], now + timedelta(days=30), now + timedelta(days=35), 2, "accepted", "Can't wait to see the lagoon!"),
            (david, stays[3], now + timedelta(days=45), now + timedelta(days=52), 4, "pending", "Bringing our own fly rods."),
            (emi, stays[6], now + timedelta(days=60), now + timedelta(days=63), 1, "accepted", "Looking forward to learning about Abemama culture."),
            (sarah, stays[1], now - timedelta(days=20), now - timedelta(days=15), 5, "completed", "It was a wonderful trip!"),
            (david, stays[10], now + timedelta(days=10), now + timedelta(days=14), 2, "declined", "Unfortunately, dates changed."),
            (emi, stays[4], now + timedelta(days=90), now + timedelta(days=97), 2, "pending", "Will we need to bring our own drinking water?"),
        ]

        for user, stay, start, end, guests, status, msg in bookings_data:
            booking = Booking(
                user_id=user.id,
                stay_id=stay.id,
                check_in=start,
                check_out=end,
                guest_count=guests,
                status=status,
                message=msg
            )
            session.add(booking)
        session.commit()

    # --- 6. REVIEWS ---
    if session.exec(select(Review)).first() is None and len(products) >= 5 and len(stays) >= 5:
        reviews_data = [
            (products[0].id, "product", 5, "Sarah Jenkins", "The craftsmanship on this Te Rau mat is unbelievable. Thick, aromatic pandanus leaves with beautiful natural dye accent patterns!"),
            (stays[0].id, "stay", 5, "David Miller", "Waking up to the calm waters of South Tarawa lagoon right outside our door was pure paradise. Warm hosts and great breakfast!"),
            (products[5].id, "product", 4, "Emily Watson", "Super fragrant and pure coconut oil. Skin feels amazingly soft."),
            (products[11].id, "product", 5, "David Miller", "Beautiful mother of pearl necklace. Fast shipping to NZ."),
            (stays[6].id, "stay", 5, "Emi Sato", "Authentic experience. The family was so welcoming and the traditional food was delicious."),
            (stays[3].id, "stay", 4, "John Smith", "Great fly fishing base. Lodge is basic but very comfortable."),
            (products[8].id, "product", 5, "Sarah Jenkins", "The outrigger canoe model is incredibly detailed. A true work of art."),
            (products[1].id, "product", 4, "Emi Sato", "Lovely fan, very well made and cooling."),
        ]

        for target_id, target_type, rating, reviewer, comment in reviews_data:
            review = Review(
                target_id=target_id,
                target_type=target_type,
                rating=rating,
                reviewer_name=reviewer,
                comment=comment
            )
            session.add(review)
        session.commit()

    # --- 7. CONVERSATIONS & MESSAGES ---
    if session.exec(select(Conversation)).first() is None:
        convs_data = [
            (sarah, tarawa_vendor, "Yes Sarah, we can customize the woven pattern with your initials!", [
                (sarah, "Hello! Can I request custom initial lettering on the Pandanus mat?"),
                (tarawa_vendor, "Bula Sarah! Yes, we can weave your initials into the border. What letters would you like?"),
                (sarah, "That's great! I would like 'S.J.' please."),
                (tarawa_vendor, "Yes Sarah, we can customize the woven pattern with your initials!")
            ]),
            (david, kiritimati_vendor, "Perfect, see you then.", [
                (david, "Hi, do you have any bonefish guides available for the dates of my booking?"),
                (kiritimati_vendor, "Mauri David, yes we do. Our expert guide Tevita is available."),
                (david, "Excellent. Please book him for the first 3 days."),
                (kiritimati_vendor, "Perfect, see you then.")
            ]),
            (emi, abemama_vendor, "I will check the shipping rates to Japan and get back to you.", [
                (emi, "Hello, is the outrigger canoe model fragile? Will it survive shipping to Tokyo?"),
                (abemama_vendor, "Mauri Emi, it is quite sturdy but we pack it very carefully in a custom wooden crate."),
                (emi, "That is reassuring. How much is the shipping cost?"),
                (abemama_vendor, "I will check the shipping rates to Japan and get back to you.")
            ])
        ]

        now = datetime.now(UTC)
        for user1, user2, last_msg, messages in convs_data:
            conv = Conversation(
                participant_names=[user1.full_name, user2.full_name],
                last_message=last_msg,
                last_message_time=now,
                unread=False
            )
            session.add(conv)
            session.commit()
            session.refresh(conv)

            for i, (sender, text) in enumerate(messages):
                msg = Message(
                    conversation_id=conv.id,
                    sender_id=sender.id,
                    text=text,
                    timestamp=now - timedelta(minutes=(len(messages) - i) * 10)
                )
                session.add(msg)
        session.commit()

    logger.info("Database successfully seeded with Kiribati dummy data!")

if __name__ == "__main__":
    import os
    os.environ['PROJECT_NAME'] = 'Kiribati Connects'
    os.environ['POSTGRES_SERVER'] = 'localhost'
    os.environ['POSTGRES_USER'] = 'postgres'
    os.environ['POSTGRES_PASSWORD'] = 'postgres'
    os.environ['POSTGRES_DB'] = 'app'
    os.environ['FIRST_SUPERUSER'] = 'admin@islandconnects.com'
    os.environ['FIRST_SUPERUSER_PASSWORD'] = 'adminpassword123'
    os.environ['SECRET_KEY'] = 'testsecretkey123456789'
    
    import sys
    sys.path.insert(0, r'd:\usman\kb-back-adm\backend')
    
    from sqlmodel import create_engine
    engine = create_engine("postgresql+psycopg://postgres:postgres@localhost/app")
    
    with Session(engine) as session:
        seed_all(session)
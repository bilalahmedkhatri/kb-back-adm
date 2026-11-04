# Kiribati Islands Platform (`islandconnects.com`) - Project Architectural Guidelines & Development Rules

This repository contains the backend and administration suite for the Kiribati E-Commerce & Hospitality Platform (`kb-back-adm`). Primary brand and domain: **`islandconnects.com`** ("Island Connects").

---

## 1. Core Architectural Guidelines

### Modular Architecture & Database Relationships
- Code is organized into 13 cohesive domain modules under `backend/app/modules/`:
  - `auth`: Authentication, JWT issuance, Google OAuth 2.0 One-Tap login (`POST /auth/google`), password recovery.
  - `users`: User profiles, registration, Google SSO fields (`google_sub`, `google_picture`), soft account deactivation (`is_active = False`), role management (`customer`, `vendor`, `admin`).
  - `vendors`: Vendor profiles, store settings, verification status (`pending`, `verified`, `rejected`), vendor analytics (`user_id -> user.id`).
  - `products`: Physical goods catalog, stock tracking, island origin, categories (`vendor_id -> user.id`).
  - `stays`: Accommodations & lodging listings, host assignments, eco-credentials (`solar_power`, `rainwater_collection`, `coral_reef_protection`), languages spoken, island location (`host_id -> user.id`).
  - `orders`: Customer checkout orders, vendor order fulfillment (`GET /orders/vendor`), line items, tracking numbers (`user_id -> user.id`).
  - `bookings`: Stay reservations, inquiry-based booking, check-in/check-out dates, guest counts (`user_id -> user.id`, `stay_id -> stay.id`).
  - `reviews`: Ratings & 4-axis feedback for products and stays (`user_id -> user.id`).
  - `conversations`: Messaging threads between users, vendors, and hosts (`user_id -> user.id`, `vendor_id -> user.id`).
  - `wishlist`: Saved products & stays per customer (`user_id -> user.id`).
  - `payments`: Payment gateway & ANZ Bank Transfer invoice logs, transaction status (`pending`, `succeeded`, `failed`, `refunded`), refund tracking (`user_id -> user.id`).
  - `guides`: Tourism & travel editorial CMS articles (`author_id -> user.id`), slug routes, topics (`Culture & Heritage`, `Travel & Nature`, `Artisan Crafts`).
  - `admin`: System-wide analytics (`GET /admin/stats`), platform audit logs (`GET /admin/audit-logs`), and oversight endpoints.

### Database & SQLModel Standards
- Use SQLModel for unified Pydantic schemas + SQLAlchemy ORM models.
- All primary keys MUST use UUID (`uuid.UUID`).
- All entities MUST link back to `user.id` via explicit Foreign Keys (`user_id`, `vendor_id`, `host_id`, `author_id`) to enforce user ownership and referential integrity.
- Datetime fields MUST default to UTC (`get_datetime_utc`).
- All persistent entities MUST include `created_at` and `updated_at` timestamps.
- Pagination MUST use standard offset parameters: `skip: int = 0`, `limit: int = 20`. Response payloads must return `{ "data": [...], "count": total_count }`.

### Payment & Currency Strategy
- Primary payment model supports ANZ Bank Transfer invoices (`anz_bank_transfer`), cash on delivery (`cash_on_delivery`), and card gateways (`stripe`, `paypal`).
- Default currency for transactions and product prices is currently `AUD` (Australian Dollar).
- **Future Roadmap**: The platform supports dynamic multi-currency conversions (USD, EUR, NZD, FJD) via external exchange rate provider APIs. All currency fields MUST remain string-configurable (`currency: str = 'AUD'`).

### Security & Role Authorization (RBAC)
- Endpoints MUST enforce explicit role checks using `CurrentUser` dependency:
  - `UserRole.ADMIN`: Full administrative override and system oversight.
  - `UserRole.VENDOR`: Resource ownership checks (`vendor_id == current_user.id` or `host_id == current_user.id`).
  - `UserRole.CUSTOMER`: User self-ownership (`user_id == current_user.id`).
- **Public Storefront Policy**: Catalog browsing (`/`, `/marketplace`, `/product/*`, `/stays`, `/stay/*`, `/guides`, `/guide/*`) is unauthenticated and open to everyone.
- **Soft Account Deactivation**: User account deactivation (`DELETE /api/v1/users/me`) sets `is_active = False` to disable login without purging historical records.

---

## 2. File Upload & Storage Strategy

- **Current Implementation**: Multipart file uploads (`POST /api/v1/utils/upload`) are stored locally in `backend/app/static/uploads` and served via FastAPI `StaticFiles` mounted at `/static`.
- **Future Storage Roadmap**: Cloudflare R2 (S3-compatible API object storage) will be integrated in future releases for production image hosting and CDN delivery.

---

## 3. Database Seeding & Mock Data Strategy

- **Seed Script Location**: `backend/app/db/seed.py`
- **Execution Command**:
  ```powershell
  cd backend
  python -m app.db.seed
  ```
- Seeds 1 Admin (`admin@kiribati.ki`), 3 Vendors (`maria@tebwa.shop`, `tione@karanga.art`, `nei@reraweaves.fi`), and 3 Customers (`john@example.com`, `sarah@example.com`, `mike@example.com`) with complete orders, bookings, reviews, conversations, wishlist items, payment logs, and tourism editorial guides (Default password: `password123`).

---

## 4. Frontend Client Generation

- When FastAPI schemas or router endpoints are modified, regenerate the frontend TypeScript client:
  ```powershell
  cd frontend
  npm run generate-client
  ```
- All client services (`ProductsService`, `OrdersService`, `VendorsService`, `StaysService`, `BookingsService`, `ReviewsService`, `ConversationsService`, `WishlistService`, `PaymentsService`, `GuidesService`, `UtilsService`) must be exported in `frontend/src/client`.

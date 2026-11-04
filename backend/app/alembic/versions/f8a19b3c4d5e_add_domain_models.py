"""Add domain models and delete items

Revision ID: f8a19b3c4d5e
Revises: e79c37f109b8
Create Date: 2026-08-16 04:59:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


revision = 'f8a19b3c4d5e'
down_revision = 'e79c37f109b8'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('DROP TABLE IF EXISTS item CASCADE')
    op.add_column('user', sa.Column('phone', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True))
    op.add_column('user', sa.Column('whatsapp', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True))
    op.add_column('user', sa.Column('avatar_url', sqlmodel.sql.sqltypes.AutoString(length=512), nullable=True))

    op.create_table(
        'product',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=False),
        sa.Column('category', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('origin_island', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('material', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column('stock', sa.Integer(), nullable=False),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
        sa.Column('images', sa.JSON(), nullable=False),
        sa.Column('vendor_id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['vendor_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_category'), 'product', ['category'], unique=False)
    op.create_index(op.f('ix_product_origin_island'), 'product', ['origin_island'], unique=False)
    op.create_index(op.f('ix_product_status'), 'product', ['status'], unique=False)
    op.create_index(op.f('ix_product_vendor_id'), 'product', ['vendor_id'], unique=False)

    op.create_table(
        'stay',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=False),
        sa.Column('price_per_night', sa.Float(), nullable=False),
        sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=False),
        sa.Column('type', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('location', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('island', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('max_guests', sa.Integer(), nullable=False),
        sa.Column('bedrooms', sa.Integer(), nullable=False),
        sa.Column('beds', sa.Integer(), nullable=False),
        sa.Column('bathrooms', sa.Integer(), nullable=False),
        sa.Column('amenities', sa.JSON(), nullable=False),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
        sa.Column('images', sa.JSON(), nullable=False),
        sa.Column('host_id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['host_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stay_island'), 'stay', ['island'], unique=False)
    op.create_index(op.f('ix_stay_type'), 'stay', ['type'], unique=False)
    op.create_index(op.f('ix_stay_status'), 'stay', ['status'], unique=False)
    op.create_index(op.f('ix_stay_host_id'), 'stay', ['host_id'], unique=False)

    op.create_table(
        'order',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('total', sa.Float(), nullable=False),
        sa.Column('subtotal', sa.Float(), nullable=False),
        sa.Column('delivery_fee', sa.Float(), nullable=False),
        sa.Column('tax', sa.Float(), nullable=False),
        sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=False),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
        sa.Column('shipping_address', sa.JSON(), nullable=False),
        sa.Column('tracking_number', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_user_id'), 'order', ['user_id'], unique=False)
    op.create_index(op.f('ix_order_status'), 'order', ['status'], unique=False)

    op.create_table(
        'orderitem',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('order_id', sa.Uuid(), nullable=False),
        sa.Column('product_id', sa.Uuid(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('image', sqlmodel.sql.sqltypes.AutoString(length=512), nullable=True),
        sa.ForeignKeyConstraint(['order_id'], ['order.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orderitem_order_id'), 'orderitem', ['order_id'], unique=False)
    op.create_index(op.f('ix_orderitem_product_id'), 'orderitem', ['product_id'], unique=False)

    op.create_table(
        'booking',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('stay_id', sa.Uuid(), nullable=False),
        sa.Column('check_in', sa.DateTime(timezone=True), nullable=False),
        sa.Column('check_out', sa.DateTime(timezone=True), nullable=False),
        sa.Column('guest_count', sa.Integer(), nullable=False),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
        sa.Column('message', sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['stay_id'], ['stay.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_booking_user_id'), 'booking', ['user_id'], unique=False)
    op.create_index(op.f('ix_booking_stay_id'), 'booking', ['stay_id'], unique=False)
    op.create_index(op.f('ix_booking_status'), 'booking', ['status'], unique=False)

    op.create_table(
        'review',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('target_id', sa.Uuid(), nullable=False),
        sa.Column('target_type', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('reviewer_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('comment', sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_target_id'), 'review', ['target_id'], unique=False)
    op.create_index(op.f('ix_review_target_type'), 'review', ['target_type'], unique=False)

    op.create_table(
        'conversation',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('participant_names', sa.JSON(), nullable=False),
        sa.Column('last_message', sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=True),
        sa.Column('last_message_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('unread', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'message',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('conversation_id', sa.Uuid(), nullable=False),
        sa.Column('sender_id', sa.Uuid(), nullable=False),
        sa.Column('text', sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_conversation_id'), 'message', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_message_sender_id'), 'message', ['sender_id'], unique=False)


def downgrade():
    op.drop_table('message')
    op.drop_table('conversation')
    op.drop_table('review')
    op.drop_table('booking')
    op.drop_table('orderitem')
    op.drop_table('order')
    op.drop_table('stay')
    op.drop_table('product')
    op.drop_column('user', 'avatar_url')
    op.drop_column('user', 'whatsapp')
    op.drop_column('user', 'phone')

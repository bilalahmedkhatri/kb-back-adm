"""add_updated_at_to_user

Revision ID: ed4f010b8886
Revises: f8a19b3c4d5e
Create Date: 2026-08-21 21:27:04.241560

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
"""add_updated_at_to_user

Revision ID: ed4f010b8886
Revises: f8a19b3c4d5e
Create Date: 2026-08-21 21:27:04.241560

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'ed4f010b8886'
down_revision = 'f8a19b3c4d5e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    op.drop_column('user', 'updated_at')

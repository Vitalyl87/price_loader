"""initial

Revision ID: 5433fe483bd1
Revises:
Create Date: 2025-04-12 21:01:34.395939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5433fe483bd1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('PriceItems',
    sa.Column('Vendor', sa.String(length=64), nullable=False),
    sa.Column('Number', sa.String(length=64), nullable=False),
    sa.Column('SearchVendor', sa.String(length=64), nullable=False),
    sa.Column('SearchNumber', sa.String(length=64), nullable=False),
    sa.Column('Description', sa.String(length=512), nullable=False),
    sa.Column('Price', sa.Numeric(precision=18, scale=2), nullable=False),
    sa.Column('Count', sa.Integer(), nullable=False),
    sa.Column('Id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('SenderConfiguration',
    sa.Column('sender', sa.String(length=128), nullable=False),
    sa.Column('vendor', sa.String(length=128), nullable=False),
    sa.Column('number', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=False),
    sa.Column('price', sa.String(length=128), nullable=False),
    sa.Column('count', sa.String(length=128), nullable=False),
    sa.Column('Id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('Id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('SenderConfiguration')
    op.drop_table('PriceItems')

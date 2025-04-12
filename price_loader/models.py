from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base model for all tables"""

    __abstract__ = True
    id: Mapped[int] = mapped_column("Id", primary_key=True, autoincrement=True)


class PriceItem(Base):
    """PriceItems table"""

    __tablename__ = "PriceItems"

    vendor: Mapped[str] = mapped_column("Vendor", String(64))
    number: Mapped[str] = mapped_column("Number", String(64))
    search_vendor: Mapped[str] = mapped_column("SearchVendor", String(64))
    search_number: Mapped[str] = mapped_column("SearchNumber", String(64))
    description: Mapped[str] = mapped_column("Description", String(512))
    price: Mapped[Decimal] = mapped_column("Price", Numeric(18, 2), nullable=False)
    count: Mapped[Integer] = mapped_column("Count", Integer)

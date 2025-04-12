from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from price_loader.models import Base


class SenderConfiguration(Base):
    """Sender price configuration table for manager"""

    __tablename__ = "SenderConfiguration"

    sender: Mapped[str] = mapped_column(String(128))
    vendor: Mapped[str] = mapped_column(String(128))
    number: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(128))
    price: Mapped[str] = mapped_column(String(128))
    count: Mapped[str] = mapped_column(String(128))

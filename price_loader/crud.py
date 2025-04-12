from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from price_loader.models import PriceItem


async def add_items_to_price(session: AsyncSession, details_list) -> int:
    saved_data = 0
    new_instances = [PriceItem(**values) for values in details_list]
    session.add_all(new_instances)
    try:
        await session.commit()
        saved_data = len(new_instances)
    except SQLAlchemyError as e:
        await session.rollback()
        raise e
    return saved_data

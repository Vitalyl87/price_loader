from sqlalchemy import Delete, Select
from sqlalchemy.ext.asyncio import AsyncSession

from price_loader.logger import logger
from price_loader.sender_configuration.models import SenderConfiguration
from price_loader.sender_configuration.schemas import ConfigurationSchema


async def rewrite_sender_configuration_to_db(
    session: AsyncSession, data: list[dict[str, str]]
):
    try:
        async with session.begin():
            await session.execute(Delete(SenderConfiguration))
            session.add_all([SenderConfiguration(**element) for element in data])

    except Exception as ex:
        logger.error(f"Error with rewrite data in db: {ex}")
        raise ex


async def get_senders(session):
    stmnt = Select(SenderConfiguration.sender)
    result = await session.execute(stmnt)
    return result.scalars().all()


async def get_configurations(session, **filter) -> list[ConfigurationSchema]:
    stmnt = Select(SenderConfiguration).filter_by(**filter)
    result = await session.execute(stmnt)
    return result.scalars().all()

from fastapi import HTTPException

from price_loader.config import settings
from price_loader.crud import add_items_to_price
from price_loader.logger import logger
from price_loader.mail_reader import MailReader
from price_loader.sender_configuration.crud import get_configurations, get_senders


async def load_details_from_mailbox(session) -> int:
    async with MailReader(
        settings.mail.login, settings.mail.password, settings.mail.server
    ) as reader:
        ids = await reader.search_letters("UNSEEN")
        if ids:
            configs = await get_dicts_for_configs(session=session)
            uploaded_details = 0
            async for data in reader.read_messages(ids, configs):
                uploaded_details += await add_items_to_price(
                    session, [x.model_dump() for x in data]
                )
            return uploaded_details
        return -1


async def get_dicts_for_configs(session):
    senders_configurations = await get_configurations(session=session)
    if len(senders_configurations) == 0:
        logger.error("Missing senders configurations")
        raise HTTPException(404, "Missing senders configurations")
    return {
        data.sender: {
            data.vendor: "vendor",
            data.number: "number",
            data.description: "description",
            data.price: "price",
            data.count: "count",
        }
        for data in senders_configurations
    }

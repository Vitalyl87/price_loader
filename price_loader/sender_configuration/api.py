import csv
from io import StringIO

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from price_loader.config import settings
from price_loader.db_helper import db_helper
from price_loader.sender_configuration.crud import (
    get_configurations,
    get_senders,
    rewrite_sender_configuration_to_db,
)
from price_loader.sender_configuration.schemas import ConfigurationSchema

router = APIRouter(
    prefix=settings.app.manager_prefix, tags=["Manage configurations for sender"]
)


@router.post("/upload-csv/", status_code=201)
async def rewrite_configuration(
    session: AsyncSession = Depends(db_helper.get_session), file: UploadFile = File(...)
) -> dict[str, str]:
    contents = await file.read()
    csv_data = StringIO(contents.decode("utf-8-sig"))

    csv_reader = csv.DictReader(csv_data, delimiter=";")
    rows = [row for row in csv_reader]
    if len(rows) > 0:
        await rewrite_sender_configuration_to_db(session=session, data=rows)
        return {"message": "Configuration added successfully"}
    else:
        return {"message": "Nothing to rewrite."}


@router.get("/senders/", status_code=200)
async def get_senders_list(
    session: AsyncSession = Depends(db_helper.get_session),
) -> list[str]:
    return await get_senders(session=session)


@router.get("/configurations/", status_code=200)
async def get_configs(
    session: AsyncSession = Depends(db_helper.get_session), sender: str = None
) -> list[ConfigurationSchema]:
    filter = {}
    if sender:
        filter["sender"] = sender
    return await get_configurations(session=session, **filter)

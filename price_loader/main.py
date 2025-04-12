from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from price_loader.config import settings
from price_loader.db_helper import db_helper
from price_loader.loader import load_details_from_mailbox
from price_loader.sender_configuration.api import router as manager_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(manager_router)


@main_app.get(settings.app.prefix, status_code=201, tags=["Load details from maibox"])
async def upload_details_to_db(
    session: AsyncSession = Depends(db_helper.get_session),
):
    objects = await load_details_from_mailbox(session)
    if objects >= 0:
        return {"message": f"{objects} details added to the database."}
    return {
        "message": "There are no messages with the attachments we are interested in."
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
    )

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from price_loader.config import settings


class Db_hepler:
    """Class for database communication"""

    def __init__(self, url: str, echo: bool) -> None:
        self.engine: AsyncEngine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self.engine.dispose()


db_helper = Db_hepler(url=str(settings.db.url), echo=settings.db.echo)

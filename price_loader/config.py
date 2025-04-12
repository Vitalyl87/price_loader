import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseModel):
    """Settings for run server"""

    host: str
    port: int
    reload: bool


class DbSettings(BaseModel):
    """Settings for db"""

    url: str
    echo: bool


class AppSettings(BaseModel):
    """Settings for app path"""

    prefix: str
    manager_prefix: str


class MailSettings(BaseModel):
    """Settings for mailbox interaction"""

    server: str
    login: str
    password: str
    port: int


class Settings(BaseSettings):
    """Settings for application"""

    db: DbSettings
    app: AppSettings
    server: ServerSettings
    mail: MailSettings

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


settings = Settings()

db_host = os.environ.get("DB_HOST", "localhost")
if db_host != "localhost":
    settings.db.url = str(settings.db.url).replace("localhost", db_host)

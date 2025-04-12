from pydantic import BaseModel


class ConfigurationSchema(BaseModel):
    """Class for ConfigurationSchema"""

    sender: str
    vendor: str
    description: str
    price: str
    count: str
    number: str

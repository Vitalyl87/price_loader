from pydantic import BaseModel, computed_field, field_validator


class DetailSchema(BaseModel):
    """Class for detail"""

    vendor: str
    description: str
    price: float
    count: int
    number: str

    @field_validator("description", mode="before")
    def cut_length(cls, val):
        if len(val) > 512:
            val = val[:512]
        return val

    @field_validator("price", mode="before")
    def change_symbol(cls, val):
        return float(val.replace(",", "."))

    @field_validator("count", mode="before")
    def get_count(cls, val):
        if "-" not in val:
            return int(val.replace(">", "").replace("<", ""))
        return int(val.split("-")[1])

    @computed_field
    def searchVendor(self) -> str:
        return "".join(char for char in self.vendor if char.isalnum()).upper()

    @computed_field
    def searchNumber(self) -> str:
        return "".join(char for char in self.number if char.isalnum()).upper()

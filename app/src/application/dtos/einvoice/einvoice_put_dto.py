from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class EInvoicePutDTO(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    einvoiceCatalogs: str = Field(..., max_length=100)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
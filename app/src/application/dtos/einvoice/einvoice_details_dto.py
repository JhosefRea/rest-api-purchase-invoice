from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class DetailsDTO(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
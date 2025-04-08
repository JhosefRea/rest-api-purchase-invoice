from pydantic import BaseModel, Field
from typing import Optional

class AddressDTO(BaseModel):
    street: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postCode: Optional[str] = Field(None, min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=50)
    

from pydantic import BaseModel, Field, ConfigDict


class UserRolModel(BaseModel):
    rol: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=100)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
    
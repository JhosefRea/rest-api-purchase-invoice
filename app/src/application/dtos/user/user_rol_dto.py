
from pydantic import BaseModel, Field, ConfigDict


class UserRolDTO(BaseModel):
    rol: str = Field(..., min_length=1, max_length=50, example="admin")
    description: str = Field(..., min_length=1, max_length=100,  example="usuario con permisos de root")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
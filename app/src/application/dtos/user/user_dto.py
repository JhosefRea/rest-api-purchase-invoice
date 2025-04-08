from pydantic import BaseModel, Field, ConfigDict, EmailStr, ConfigDict, BeforeValidator 
from typing import Optional, Annotated
from app.src.application.dtos.user.user_rol_dto import UserRolDTO


PyObjectId = Annotated[str, BeforeValidator(str)]

class UserDTO(BaseModel):
    mongo_id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(..., min_length=1, max_length=100, example="Zlatan")
    email: EmailStr = Field(..., min_length=1, max_length=100, example="zlatan@empresa.ec")
    password: str = Field(..., min_length=3, max_length=140)
    userRol: Optional[UserRolDTO] = Field(...)
    status: str = Field(..., example="active")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from app.src.domain.users.user_rol_model import UserRolModel

class UserModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=3, max_length=140)
    userRol: Optional[UserRolModel] = Field(...)
    status: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    
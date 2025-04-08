from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from typing import Any

# Back-end
from app.src.application.services.user_service import PostUserService, PutUserService, DeleteUserService, GetUserService, GetAllUserService
from app.src.infrastructure.adapters.outbound.persistence.repository.user.put_user_repository import PutUserRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.user.post_user_repository import PostUserRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.user.delete_user_repository import DeleteUserRepository 
from app.src.infrastructure.adapters.outbound.persistence.repository.user.get_user_repository import GetUserRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.user.getall_user_repository import GetAllUserRepository


from app.src.application.dtos.user.user_dto import UserDTO
from app.src.domain.users.user_model import UserModel


router = APIRouter()

repository_post = PostUserRepository()
service_post = PostUserService(repository_post)

repository_put = PutUserRepository()
service_put = PutUserService(repository_put)

repository_delete = DeleteUserRepository()
service_delete = DeleteUserService(repository_delete)

repository_get = GetUserRepository()
service_get = GetUserService(repository_get)

repository_getAll = GetAllUserRepository()
service_getAll = GetAllUserService(repository_getAll)
'''
@router.get("/", response_model=list[dict[str, Any]])
async def get_all_users():
    try:
        invoices = await service_getAll.invoke()
        return invoices
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail="Invoices not found")
'''
#back-end

@router.post("/", response_model=UserDTO)
async def create_user(user_dto: UserDTO):
    try:
        # Convertir DTO a dict con alias y crear el modelo EInvoice en DB
        user = UserModel(**user_dto.model_dump(by_alias=True))

        # Llamar al servicio para guardar en MongoDB
        return await service_post.invoke(user)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(e.errors()),
        )

@router.put("/{id}", response_model=UserDTO)
async def update_user(id: str, user_dto: UserDTO):
    try:
        # Convertir DTO a dict con alias y crear el modelo EInvoice en DB
        user = UserModel(**user_dto.model_dump(by_alias=True))
        print("___controller____PUT USER____", user, "*****", id)

        # Llamar al servicio para guardar en MongoDB
        return await service_put.invoke(id, user)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(e.errors()),
        )

@router.delete("/{id}", response_model=UserDTO)
async def delete_user(id: str):
    try:
        # Llamar al servicio para eliminar en MongoDB
        return await service_delete.invoke(id)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(e.errors()),
        )    


@router.get("/{id}", response_model=UserDTO)
async def get_user(id: str):
    try:
        # Llamar al servicio para obtener en MongoDB
        return await service_get.invoke(id)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(e.errors()),
        )

@router.get("/", response_model=list[UserDTO])
async def get_all_users():
    try:
        users = await service_getAll.invoke()
        if not users:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        # Convertir cada usuario a un diccionario usando model_dump
        users_dict = [user.model_dump(by_alias=True) for user in users]
        return users_dict

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(e.errors()),
        )
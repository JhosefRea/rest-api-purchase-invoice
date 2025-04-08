from starlette.responses import JSONResponse
from app.src.infrastructure.adapters.outbound.persistence.repository.user.post_user_repository import PostUserRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.user.put_user_repository import PutUserRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.user.delete_user_repository import DeleteUserRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.user.get_user_repository import GetUserRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.user.getall_user_repository import GetAllUserRepository
from app.src.domain.users.user_model import UserModel
from app.src.application.dtos.user.user_dto import UserDTO


class PostUserService:
    def __init__(self, repository: PostUserRepository):
        self.repository = repository

    async def invoke(self, user: UserModel) -> UserDTO:
        # Aquí se puede añadir lógica adicional en el futuro.
        return await self.repository.post_user(user)

class PutUserService:
    def __init__(self, repository: PutUserRepository):
        self.repository = repository

    async def invoke(self, id: str, user: UserModel) -> UserDTO:
        # Lógica de negocio antes de actualizar el usuario
        return await self.repository.put_user(id, user)

class DeleteUserService:
    def __init__(self, repository: DeleteUserRepository):
        self.repository = repository

    async def invoke(self, id: str) -> JSONResponse:
        # Lógica de negocio antes de eliminar usuario
        return await self.repository.delete_user(id)

class GetUserService:
    def __init__(self, repository: GetUserRepository):
        self.repository = repository

    async def invoke(self, id: str) -> JSONResponse:
        # Lógica de negocio antes de obtener el usuario
        return await self.repository.get_user(id)

class GetAllUserService:
    def __init__(self, repository: GetAllUserRepository):
        self.repository = repository

    async def invoke(self) -> list[UserDTO]:
        # Lógica de negocio antes de obtener el usuario
        return await self.repository.get_all_users()

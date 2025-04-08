from abc import ABC, abstractmethod
from app.src.application.dtos.user.user_dto import UserDTO
from app.src.domain.users.user_model import UserModel


class PutUserUC(ABC):
    @abstractmethod
    def put_user(self, id: str, user: UserModel) -> UserDTO:
        raise NotImplementedError


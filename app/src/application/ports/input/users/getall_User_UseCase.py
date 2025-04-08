from abc import ABC, abstractmethod
from app.src.application.dtos.user.user_dto import UserDTO


class GetAllUserUC(ABC):
    @abstractmethod
    def get_all_users() -> list[UserDTO]:
        raise NotImplementedError


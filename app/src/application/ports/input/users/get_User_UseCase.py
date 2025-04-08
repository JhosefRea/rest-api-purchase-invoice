from abc import ABC, abstractmethod
from app.src.application.dtos.user.user_dto import UserDTO


class GetUserUC(ABC):
    @abstractmethod
    def get_user(self, id: str) -> UserDTO:
        raise NotImplementedError


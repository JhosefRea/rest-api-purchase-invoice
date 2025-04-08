from abc import ABC, abstractmethod
from app.src.application.dtos.user.user_dto import UserDTO
from app.src.domain.users.user_model import UserModel


class PostUserUC(ABC):
    @abstractmethod
    def post_user(self, invoiceData: UserModel) -> UserDTO:
        raise NotImplementedError


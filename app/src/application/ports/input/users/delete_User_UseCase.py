from abc import ABC, abstractmethod
from starlette.responses import JSONResponse


class DeleteUserUC(ABC):
    @abstractmethod
    def delete_user(self, id: str) -> JSONResponse:
        raise NotImplementedError


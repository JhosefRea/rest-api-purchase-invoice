from abc import ABC, abstractmethod
from typing import Any


class EInvoiceGetAllOutputPort(ABC):
    @abstractmethod
    async def get_einvoices_ws(self) -> list[dict[str, Any]] :
        raise NotImplementedError
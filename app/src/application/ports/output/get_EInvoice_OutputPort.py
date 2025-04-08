'''
antes de febrero escribí esto

Clase Abstracta que se usa en adaptador de salida (API REST y para el MONGO).
GET ALL - API REST / MONGO
GET BY ID - API REST / MONGO
POST - MONGO
UPDATE - MONGO
'''
from abc import ABC, abstractmethod
from typing import Any


class EInvoiceGetOutputPort(ABC):
    @abstractmethod
    async def get_einvoice_ws(self, id: Any) -> dict[str, Any] :
        raise NotImplementedError

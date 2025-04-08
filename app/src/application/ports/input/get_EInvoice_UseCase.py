from abc import ABC, abstractmethod
from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO


class GetEInvoiceHandlerUC(ABC):
    @abstractmethod
    def get_einvoice() -> EInvoiceDTO:
        raise NotImplementedError

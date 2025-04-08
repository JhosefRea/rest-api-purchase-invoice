from abc import ABC, abstractmethod
from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO


class GetAllEInvoicesUC(ABC):
    @abstractmethod
    def get_all_einvoices() -> list[EInvoiceDTO]:
        raise NotImplementedError


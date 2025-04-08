from abc import ABC, abstractmethod
from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO
from app.src.domain.einvoices.einvoice_model import EInvoiceModel


class PostEInvoiceUC(ABC):
    @abstractmethod
    def post_einvoice(self, invoiceData: EInvoiceModel) -> EInvoiceDTO:
        raise NotImplementedError

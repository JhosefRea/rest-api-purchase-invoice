from abc import ABC, abstractmethod
from app.src.application.dtos.einvoice.einvoice_put_dto import EInvoicePutDTO
from app.src.domain.einvoices.einvoice_model import EInvoiceModel


class PutEInvoiceUC(ABC):
    @abstractmethod
    def put_einvoice(self, invoiceData: EInvoiceModel) -> EInvoicePutDTO:
        raise NotImplementedError

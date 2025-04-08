from abc import ABC, abstractmethod
from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO

'''
Este handler es para filtrar las facturas del WS y del back-end
Propósito: si la factura existe en el bac-end, no debe traer del WS
'''

class GetAllEInvoicesHandlerUC(ABC):
    @abstractmethod
    def get_all_filter_einvoices() -> list[EInvoiceDTO]:
        raise NotImplementedError

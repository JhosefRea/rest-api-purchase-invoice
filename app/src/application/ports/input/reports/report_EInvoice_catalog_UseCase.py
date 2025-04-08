from abc import ABC, abstractmethod
from app.src.application.dtos.report.report_einvoice_x_catalog_dto import ReportEInvoiceCatalogDTO


class ReportEInvoiceCatalogUC(ABC):
    @abstractmethod
    def report_einvoices_catalog_Agregations(self) -> list[ReportEInvoiceCatalogDTO]:
        raise NotImplementedError

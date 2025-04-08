from app.src.infrastructure.adapters.outbound.persistence.repository.report.report_einvoice_catalog_repository import ReportEinvoiceCatalogRepository
from app.src.application.dtos.report.report_einvoice_x_catalog_dto import ReportEInvoiceCatalogDTO


class ReportEinvoiceCatalogService:
    def __init__(self, repository: ReportEinvoiceCatalogRepository):
        self.repository = repository

    async def invoke(self) -> list[ReportEInvoiceCatalogDTO]:
        # Lógica de negocio antes de obtener el usuario
        return await self.repository.report_einvoices_catalog_Agregations()

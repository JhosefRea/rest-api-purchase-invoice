from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.getall_EInvoice_handler_repository import GetAllEInvoicesHandlerRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.get_EInvoice_handler_repository import GetEInvoiceHandlerRepository

from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO

class GetAllEIenvoiceHandlerService:
    def __init__(self, repository: GetAllEInvoicesHandlerRepository):
        self.repository = repository

    async def invoke(self) -> list[EInvoiceDTO]:
        # Lógica de negocio antes de obtener la factura
        return await self.repository.get_all_filter_einvoices()

class GetEInvoiceHandlerService:
    def __init__(self, repository: GetEInvoiceHandlerRepository):
        self.repository = repository

    async def invoke(self, id: str) -> EInvoiceDTO:
        # Aquí se puede añadir lógica adicional en el futuro.
        return await self.repository.get_einvoice(id)
    

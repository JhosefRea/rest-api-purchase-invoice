from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.post_EInvoice_repository import PostEInvoiceRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.getall_einvoice_repository import GetAllEInvoiceRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.put_EInvoice_repository import PutEInvoiceRepository

from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO
from app.src.application.dtos.einvoice.einvoice_put_dto import EInvoicePutDTO
from app.src.domain.einvoices.einvoice_model import EInvoiceModel


class PostEInvoiceService:
    def __init__(self, repository: PostEInvoiceRepository):
        self.repository = repository

    async def invoke(self, einvoice: EInvoiceModel) -> EInvoiceDTO:
        # Aquí se puede añadir lógica adicional en el futuro.
        return await self.repository.post_einvoice(einvoice)


class GetAllEIenvoiceService:
    def __init__(self, repository: GetAllEInvoiceRepository):
        self.repository = repository

    async def invoke(self) -> list[EInvoiceDTO]:
        # Lógica de negocio antes de obtener la factura
        return await self.repository.get_all_einvoices()
    

class PutEInvoiceService:
    def __init__(self, repository: PutEInvoiceRepository):
        self.repository = repository

    async def invoke(self, id: str, einvoice: EInvoiceModel) -> EInvoicePutDTO:
        # Aquí se puede añadir lógica adicional en el futuro.
        return await self.repository.put_einvoice(id, einvoice)

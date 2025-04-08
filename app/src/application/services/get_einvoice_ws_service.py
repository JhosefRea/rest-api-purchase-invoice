from ...infrastructure.adapters.outbound.persistence.get_EInvoice_ws_repository import EInvoiceRepositoryWS
from ...infrastructure.adapters.outbound.persistence.getall_EInvoices_ws_repository import EInvoicesRepositoryWS
# from ...domain.einvoices.einvoice_model import EInvoiceModel

'''
aquí habría otros GET
las llamo invoice para distinguir y generalizar a las facturas:
backend: einvoice
rest api: invoice
front: 
'''


# WS
class GetInvoiceService:
    def __init__(self, repository: EInvoiceRepositoryWS):
        self.repository = repository

    async def invoke(self, id: str) -> dict[str, any]:
        # Aquí se puede añadir lógica adicional
        # como cambiar keys de json segun corresponda con las propiedades de EInvoice Model
        # No se retorna un EInvoice Model
        # pero tocaría cambbiar las validaciones-excepciones, ponerlas aquí y no en el controller
        return await self.repository.get_einvoice_ws(id)

# WS
class GetAllInvoicesService:
    def __init__(self, repository: EInvoicesRepositoryWS):
        self.repository = repository

    async def invoke(self) -> list[dict[str, any]]:
        # Aquí se puede añadir lógica adicional en el futuro.
        return await self.repository.get_einvoices_ws()

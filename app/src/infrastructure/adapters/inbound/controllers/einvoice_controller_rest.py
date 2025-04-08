from fastapi import APIRouter, HTTPException, status, Path, Body
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from httpx import HTTPStatusError
from typing import Any
from bson import ObjectId

# WS
from ...outbound.persistence.get_EInvoice_ws_repository import EInvoiceRepositoryWS
from ...outbound.persistence.getall_EInvoices_ws_repository import EInvoicesRepositoryWS
from .....application.services.get_einvoice_ws_service import GetInvoiceService
from .....application.services.get_einvoice_ws_service import GetAllInvoicesService

# Back-end - Handlers
from app.src.application.services.einvoice_handler_service import GetAllEIenvoiceHandlerService, GetEInvoiceHandlerService
from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.getall_EInvoice_handler_repository import GetAllEInvoicesHandlerRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.get_EInvoice_handler_repository import GetEInvoiceHandlerRepository

#Back-end 
from app.src.application.services.einvoice_service import PostEInvoiceService, GetAllEIenvoiceService, PutEInvoiceService
from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.post_EInvoice_repository import PostEInvoiceRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.getall_einvoice_repository import GetAllEInvoiceRepository
from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.put_EInvoice_repository import PutEInvoiceRepository
from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO
from app.src.application.dtos.einvoice.einvoice_put_dto import EInvoicePutDTO
from app.src.domain.einvoices.einvoice_model import EInvoiceModel


router = APIRouter()
#WS
repository_WS_getByid = EInvoiceRepositoryWS()
service_ws_getByid = GetInvoiceService(repository_WS_getByid)

repository_WS_getAll = EInvoicesRepositoryWS()
service_ws_getAll = GetAllInvoicesService(repository_WS_getAll)

#BACK-END
repository_post = PostEInvoiceRepository()
service_post = PostEInvoiceService(repository_post)

repository_getAll = GetAllEInvoiceRepository()
service_getAll = GetAllEIenvoiceService(repository_getAll)

repository_put = PutEInvoiceRepository()
service_put = PutEInvoiceService(repository_put)

#HANDLERS
repository_handler_getByid = GetEInvoiceHandlerRepository()
service_handler_getByid = GetEInvoiceHandlerService(repository_handler_getByid)

repository_getall_handler = GetAllEInvoicesHandlerRepository()
service_getall_handler = GetAllEIenvoiceHandlerService(repository_getall_handler)



# WS
@router.get("/ws/{_id}", response_model=dict[str, Any])
async def get_invoice_ws(
    _id: str = Path(..., title="ID de la factura", description="### **El param _id debe ser de tipo ObjectId.** ###"),
    tags="una factura", summary="obtiene una factura del WS", description="obtiene una factura específica por **_id**, que debe ser un **ObjectId**"
):
    try:
        id = ObjectId(_id)
        invoice = await service_ws_getByid.invoke(id)
        return invoice
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail="Invoice not found")

# WS


@router.get("/ws/", response_model=list[dict[str, Any]])
async def get_all_invoices_ws(
    tags=["facturas"], summary="obtiene facturas.", description="obtiene una lista de facturas."
):
    try:
        invoices = await service_ws_getAll.invoke()
        return invoices
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail="Invoices not found")


#back-end
@router.post("/", response_model=EInvoiceDTO)
async def create_invoice(invoice_dto: EInvoiceDTO = Body(...)):
    print("_________einvoice_controller_______POST___")
    try:
        # Convertir DTO a dict con alias y crear el modelo EInvoice en DB
        #einvoice es instancia del modelo, es un modelo
        einvoice = EInvoiceModel(**invoice_dto.model_dump(by_alias=True)) 

        # Llamar al servicio para guardar en MongoDB
        return await service_post.invoke(einvoice)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(e.errors()),
        )
    
    
@router.get("/", response_model=list[EInvoiceDTO])
async def get_all_invoices():
    try:
        einvoices = await service_getAll.invoke()
        einvoices_dict = [einvoice.model_dump(by_alias=True) for einvoice in einvoices]

        return einvoices_dict
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail="Invoices not found")


@router.put("/{id}", response_model=EInvoicePutDTO)
async def update_einvoice(
    einvoice_dto: EInvoicePutDTO, 
    id: str = Path(..., title="Código de la factura", description="### **El param id debe ser de tipo string.** ###"),
    description="**id** es el **código de la factura**"
    ):
    try:
        # Convertir DTO a dict con alias y crear el modelo EInvoice en DB
        einvoice = EInvoiceModel(**einvoice_dto.model_dump(by_alias=True))
        print("___controller____PUT___", einvoice, "*****", id)

        # Llamar al servicio para guardar en MongoDB
        return await service_put.invoke(id, einvoice)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(e.errors()),
        )
     

#HANDLER
@router.get("/handler/{id}", response_model=EInvoiceDTO)
async def get_invoice(
    id: str = Path(..., title="ID de la factura", description="### **El param _id debe ser de tipo ObjectId.** ###"),
):
    try:
        # facturaen el backend
        einvoice = await service_handler_getByid.invoke(id)
        if einvoice:
            return einvoice
        
        # Si no encontramos la factura en el backend, la buscamos en el WS
        invoice = await service_ws_getByid.invoke(id)
        if invoice:
            return invoice
    
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail="Invoice not found")
        

#HANDLER
@router.get("/handler/", response_model=list[EInvoiceDTO])
async def get_all_invoices_ws_backend():
    try:
        invoices = await service_getall_handler.invoke()
        print("controller GETALL hander DESPUES________________")

        #se obtiene una lista de DTOS
        einvoices_dto = [invoice for invoice in invoices]
        print(f'controller___Tipo de dato de einvoices, y es un DTO: {type(einvoices_dto)}')


        # Devolver la lista de objetos EInvoiceDTO
        return einvoices_dto

        # Se usa `model_dump()` para convertir objetos Pydantic a diccionarios en Pydantic v2
        #einvoices_dict = [user.model_dump(by_alias=True) for user in invoices]

    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail="Invoices not found")
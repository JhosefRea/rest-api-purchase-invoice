from fastapi import HTTPException
from app.src.infrastructure.adapters.outbound.persistence.getall_EInvoices_ws_repository import EInvoicesRepositoryWS 
from app.src.application.ports.input.getall_EInvoices_handler_UseCase import GetAllEInvoicesHandlerUC
from app.src.infrastructure.adapters.outbound.persistence.repository.einvoices.getall_einvoice_repository import GetAllEInvoiceRepository
from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO
from app.src.application.dtos.einvoice.einvoice_details_dto import DetailsDTO
from app.src.infrastructure.config.database.database import mongodb



class GetAllEInvoicesHandlerRepository(GetAllEInvoicesHandlerUC):
    
    def __init__(self):
        self.invoices_ws = EInvoicesRepositoryWS()
        self.einvoices_backend = GetAllEInvoiceRepository()
        self.collection = mongodb.get_collection("e-invoices")


    async def get_all_filter_einvoices(self) -> list[EInvoiceDTO]:
        invoices_ws = await self.invoices_ws.get_einvoices_ws()
        mongo_einvoices_cursor = self.collection.find()
        mongo_einvoices = await mongo_einvoices_cursor.to_list(100)

        # Convertir las facturas de MongoDB a DTO
        mongo_einvoices = [
            EInvoiceDTO(
                _id=str(einvoice["_id"]),
                id=einvoice["id"],
                createdAt=einvoice["createdAt"],
                paymentDue=einvoice["paymentDue"],
                description=einvoice["description"],
                paymentTerms=einvoice["paymentTerms"],
                clientName=einvoice["clientName"],
                clientEmail=einvoice["clientEmail"],
                status=einvoice["status"],
                senderAddress=einvoice["senderAddress"],
                clientAddress=einvoice["clientAddress"],
                items=[DetailsDTO(**item) for item in einvoice["items"]],
                total=einvoice["total"],
                einvoiceCatalogs=einvoice.get("einvoiceCatalogs", None)  # Solo estará en MongoDB
            )
            for einvoice in mongo_einvoices
        ]
        #ESTO ES CON DATOS DEL WS COMO DICCIONARIO (EN JSON SE LOS OBTIENE DEL WS)
        ws_invoices = [
            {
                "_id": invoice["_id"],  
                "id": invoice["id"],
                "createdAt": invoice["createdAt"],
                "paymentDue": invoice["paymentDue"],
                "description": invoice["description"],
                "paymentTerms": invoice["paymentTerms"],
                "clientName": invoice["clientName"],
                "clientEmail": invoice["clientEmail"],
                "status": invoice["status"],
                "senderAddress": invoice["senderAddress"],
                "clientAddress": invoice["clientAddress"],
                "items": invoice["items"], 
                "total": invoice["total"],
            }
            for invoice in invoices_ws
        ]

        # Ahora compara las facturas del WS con las de MongoDB
        all_invoices = []

        # Primero agregar las facturas de MongoDB
        all_invoices.extend(mongo_einvoices)

        # Luego agregar las facturas del WS solo si no existen en MongoDB
        # Comparando las facturas del WS (diccionario) con las de MongoDB (objeto DTO)
        for ws_invoice in ws_invoices:
            # Accede correctamente a los campos del diccionario ws_invoice
            ws_invoice_id = ws_invoice["id"]
            
            # Compara con los objetos de MongoDB, accediendo a los atributos con notación de punto
            if not any(invoice.id == ws_invoice_id for invoice in mongo_einvoices):
                all_invoices.append(ws_invoice)


        #retorn DTOS
        return all_invoices 


        ##########
        #return [self.document_to_invoice(doc) for doc in backend_invoices]


    '''
    ESTO ES CON DATOS DEL WS TRANSFORMANDO A DTO
        ws_einvoices = [
            EInvoiceDTO(
                _id=str(invoice["_id"]),  # No existe en MongoDB
                id=invoice["id"],
                createdAt=invoice["createdAt"],
                paymentDue=invoice["paymentDue"],
                description=invoice["description"],
                paymentTerms=invoice["paymentTerms"],
                clientName=invoice["clientName"],
                clientEmail=invoice["clientEmail"],
                status=invoice["status"],
                senderAddress=invoice["senderAddress"],
                clientAddress=invoice["clientAddress"],
                items=[DetailsDTO(**item) for item in invoice["items"]],
                total=invoice["total"],
            )
            for invoice in einvoices_ws
        ]
        

        # Ahora compara las facturas del WS con las de MongoDB
        all_invoices = []

        # Primero agregar las facturas de MongoDB
        all_invoices.extend(mongo_einvoices)

        # Luego agregar las facturas del WS solo si no existen en MongoDB
        for ws_invoice in ws_einvoices:
            # Compara si la factura del WS ya existe en MongoDB (por ID en este caso)
            if not any(invoice.id == ws_invoice.id for invoice in mongo_einvoices):
                all_invoices.append(ws_invoice)

        return all_invoices

    '''

    '''def document_to_invoice(self, document: dict) -> EInvoiceDTO:
        sender_address_data = document.get("senderAddress", {})
        client_address_data = document.get("clientAddress", {})

        sender_address = AddressDTO(
            street=sender_address_data.get("street", "Unknown Street"),
            city=sender_address_data.get("city", "Unknown City"),
            postCode=sender_address_data.get("postCode", "00000"),
            country=sender_address_data.get("country", "Unknown Country")
        )

        client_address = AddressDTO(
            street=client_address_data.get("street", "Unknown Street"),
            city=client_address_data.get("city", "Unknown City"),
            postCode=client_address_data.get("postCode", "00000"),
            country=client_address_data.get("country", "Unknown Country")
        )

        details = [DetailsDTO(**item) for item in document.get("items", [])]

        return EInvoiceDTO(
            _id=document.get("_id"), #o document["_id"]
            id=document.get("id", "default_id"),
            createdAt=document.get("createdAt", datetime.now()),
            paymentDue=document.get("paymentDue", datetime(1970, 1, 1)),
            description=document.get("description", "default_description"),
            paymentTerms=document.get("paymentTerms", 30),
            clientName=document.get("clientName", "default_client_name"),
            clientEmail=document.get("clientEmail", "default_client_email"),
            status=document.get("status", "default_status"),
            senderAddress=sender_address,
            clientAddress=client_address,
            items=details,
            total=document.get("total", 1),
            einvoiceCatalogs=document.get("einvoiceCatalogs")
        )'''
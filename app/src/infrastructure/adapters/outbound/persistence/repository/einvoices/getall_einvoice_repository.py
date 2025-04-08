from fastapi import HTTPException
from datetime import datetime
from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO
from app.src.application.dtos.einvoice.einvoice_details_dto import DetailsDTO
from app.src.application.dtos.einvoice.einvoice_address_dto import AddressDTO
from app.src.application.ports.input.einvoices.getall_Einvoice_UseCase import GetAllEInvoicesUC
from app.src.infrastructure.config.database.database import mongodb



class GetAllEInvoiceRepository(GetAllEInvoicesUC):
    def __init__(self):
        self.collection = mongodb.get_collection("e-invoices")

    async def get_all_einvoices(self) -> list[EInvoiceDTO]:
        documents = await self.collection.find().to_list(100)
        return [self.document_to_invoice(doc) for doc in documents]

    def document_to_invoice(self, document: dict) -> EInvoiceDTO:
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
            paymentDue=document.get("paymentDue", datetime(1958, 1, 1)),
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
        )

    
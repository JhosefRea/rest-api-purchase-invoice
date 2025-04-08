from bson import ObjectId
from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO
from app.src.application.ports.input.einvoices.post_EInvoice_UseCase import PostEInvoiceUC
from app.src.infrastructure.config.database.database import mongodb
from app.src.domain.einvoices.einvoice_model import EInvoiceModel


class PostEInvoiceRepository(PostEInvoiceUC):
    def __init__(self):
        self.collection = mongodb.get_collection("e-invoices")

    async def post_einvoice(self, einvoice: EInvoiceModel) -> EInvoiceDTO:
        print("______post_einvoice_repository.py_____", einvoice)
        
        # Preparar el dict para MongoDB (incluye agregar _id a los items si no existen)
        invoice_dict = self._prepare_invoice_dict(einvoice)

        # Inserta el documento en la base de datos y es un bjeto InsertOneResult, de Mongo
        await self.collection.insert_one(invoice_dict)

        # Retorna un InvoicePostDTO basado en el documento almacenado
        return EInvoiceDTO(**invoice_dict)

    def _prepare_invoice_dict(self, einvoice: EInvoiceModel | dict) -> dict:
        # Convertir a dict si es un modelo
        if isinstance(einvoice, EInvoiceModel):
            invoice_dict = einvoice.model_dump(by_alias=True)
        else:
            invoice_dict = einvoice

        # Asegurarse de que todos los subdocumentos en "items" tengan un `_id`
        for item in invoice_dict.get("items", []):
            if "_id" not in item:
                item["_id"] = ObjectId()

        # Elimina el campo _id del documento principal si está presente porque fastAPI
        # (a través de Pydantic) no sbae cómo serelizarlo a Json
        #invoice_dict.pop("_id", None) CREOQ NO SIRVE NI LO NECESITO

        return invoice_dict


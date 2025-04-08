from fastapi import HTTPException
from app.src.application.dtos.einvoice.einvoice_put_dto import EInvoicePutDTO
from app.src.application.ports.input.einvoices.put_EInvoice_UseCase import PutEInvoiceUC
from app.src.infrastructure.config.database.database import mongodb
from app.src.domain.einvoices.einvoice_model import EInvoiceModel


class PutEInvoiceRepository(PutEInvoiceUC):
    def __init__(self):
        self.collection = mongodb.get_collection("e-invoices")

    async def put_einvoice(self, id: str, einvoice: EInvoiceModel) -> EInvoicePutDTO:
        try:
            einvoice_codeNumber = id
            # Preparar el dict para MongoDB (convierte el modelo UserModel a dict)
            einvoice_dict = einvoice.model_dump()

            # Campos a actualizar
            update_to_fields_dict = {
                "einvoiceCatalogs": einvoice_dict.get("einvoiceCatalogs")
            }

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid ID: {str(e)}")
        
        
        try:
            # Actualizar el documento en la base de datos
            update_result = await self.collection.update_one(
                {"id": einvoice_codeNumber}, 
                {"$set": update_to_fields_dict}
            )

            # Si no se encontró la factura devolver error 404
            if not update_result:
                raise HTTPException(status_code=404, detail="Einvoice not found")

            # Buscar la factura actualizado
            updated_einvoice = await self.collection.find_one({"id": einvoice_codeNumber})

            # Si la factura no se encuentra después de la actualización
            if updated_einvoice is None:
                raise HTTPException(status_code=404, detail="Einvoice not found after update")

            # Asegurarse de convertir _id a string antes de pasar al DTO
            updated_einvoice["_id"] = str(updated_einvoice["_id"])

            # Retornar el DTO del usuario actualizado
            return EInvoicePutDTO(**updated_einvoice)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

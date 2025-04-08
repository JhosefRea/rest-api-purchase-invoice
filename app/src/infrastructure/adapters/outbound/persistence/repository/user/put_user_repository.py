from fastapi import HTTPException
from httpx import HTTPStatusError, RequestError
from bson import ObjectId
from app.src.application.dtos.user.user_dto import UserDTO
from app.src.application.ports.input.users.put_User_UseCase import PutUserUC
from app.src.infrastructure.config.database.database import mongodb
from app.src.domain.users.user_model import UserModel


class PutUserRepository(PutUserUC):
    def __init__(self):
        self.collection = mongodb.get_collection("users")

    async def put_user(self, id: str, user: UserModel) -> UserDTO:
        try:
            # Convertir el id a ObjectId
            object_id = ObjectId(id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid ID format: {str(e)}")
        
        # Preparar el dict para MongoDB (convierte el modelo UserModel a dict)
        user_dict = user.model_dump()

        try:
            # Actualizar el documento en la base de datos
            update_result = await self.collection.update_one(
                {"_id": object_id}, 
                {"$set": user_dict}
            )

            # Si no se encontró el usuario, devolver error 404
            if update_result.matched_count == 0:
                raise HTTPException(status_code=404, detail="User not found")

            # Buscar el usuario actualizado
            updated_user = await self.collection.find_one({"_id": object_id})

            # Si el usuario no se encuentra después de la actualización
            if updated_user is None:
                raise HTTPException(status_code=404, detail="User not found after update")

            # Asegurarse de convertir _id a string antes de pasar al DTO
            updated_user["_id"] = str(updated_user["_id"])

            # Retornar el DTO del usuario actualizado
            return UserDTO(**updated_user)

        except Exception as e:
            # Si ocurre algún error, lanzamos una excepción HTTP con detalle del error
            raise HTTPException(status_code=500, detail=f"An error occurred/: {str(e)}")

       
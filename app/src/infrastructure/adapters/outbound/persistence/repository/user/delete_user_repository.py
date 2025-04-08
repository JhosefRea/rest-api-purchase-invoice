
from fastapi import HTTPException
from bson import ObjectId
from starlette.responses import JSONResponse
from app.src.application.ports.input.users.delete_User_UseCase import DeleteUserUC
from app.src.infrastructure.config.database.database import mongodb
from app.src.domain.users.user_model import UserModel



class DeleteUserRepository(DeleteUserUC):
    def __init__(self):
        self.collection = mongodb.get_collection("users")

    async def delete_user(self, id: str) -> JSONResponse:
        try:
            # Convertir el id a ObjectId
            object_id = ObjectId(id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid ID format: {str(e)}")
        
        try:
            # Buscamos el usuario para ver si existe
            user = await self.collection.find_one({"_id": object_id})
            print("_____delete_user______", user)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            

            # Eliminado lógico
            await self.collection.update_one(
                {"_id": object_id}, 
                {"$set": {**user, "status": "inactive"}}
            )

            # Si no se encontró el usuario, devolver error 404
            if user is 0:
                raise HTTPException(status_code=404, detail="User not found")
            

            return JSONResponse(
                content={"detail": "User deleted successfully."},
            )
   
        except Exception as e:
            # Si ocurre algún error, lanzamos una excepción HTTP con detalle del error
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

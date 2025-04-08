from passlib.context import CryptContext

from app.src.domain.users.user_model import UserModel
from motor.motor_asyncio import AsyncIOMotorDatabase


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    """Hashea la contraseña usando bcrypt."""
    return pwd_context.hash(password)

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("users")

    async def get_user_by_username(self, username: str):
        """Busca un usuario por su nombre de usuario"""
        user_data = await self.collection.find_one({"name": username})
        if user_data:
            return UserModel(**user_data)
        return None

    async def create_user(self, user: UserModel):
        """Crea un nuevo usuario en la base de datos"""
        user_dict = user.dict()
        #Hashear la contraseña antes de guardarla
        hashed_password = hash_password(user_dict["password"])
        user_dict["password"] = hashed_password
        await self.collection.insert_one(user_dict)

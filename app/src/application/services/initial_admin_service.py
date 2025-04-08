from app.src.domain.users.user_model import UserModel
from app.src.infrastructure.adapters.outbound.persistence.repository.user.initial_admin_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_admin_user(self):
        """Verifica si el usuario admin existe y lo crea si no existe"""
        admin_user = await self.user_repo.get_user_by_username("admin")
        print(f"Resultado dela búsqueda: {admin_user}")  # 🟢 DEBUG
        if not admin_user:
            admin_username = "admin"
            admin_email = "admin@admin.com"        
            userRol = {"rol": "admin", "description": "Usuario root"}
            admin = UserModel(name=admin_username, email=admin_email, password="123",  userRol=userRol,  status="active")      
            await self.user_repo.create_user(admin)
            print("Usuario administrador creado con éxito.")
        else:
            print("El usuario administrador ya existe.")

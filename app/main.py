from fastapi import FastAPI

from .src.infrastructure.adapters.inbound.routers.router_inbound import RouterEInvoices
from .src.infrastructure.adapters.inbound.routers.router_inbound import RouterUsers
from .src.infrastructure.adapters.inbound.routers.router_inbound import RouterReportsEinvoices
from .src.infrastructure.adapters.inbound.routers.router_inbound import RouterLogin


from config.cors_config import custom_cors_rest, custom_cors_browser
from .src.infrastructure.config.middlewares.logging_middleware_rest import log_requests
from .src.infrastructure.config.middlewares.Custom_Middleware_Rest import CustomMiddlewareRest
from .src.infrastructure.config.middlewares.custom_Middleware_Preflight import CustomMiddlewarePreflight
from .src.infrastructure.config.middlewares.custom_Middleware_WithoutOrigin import CustomMiddlewareWitoutOrigin


from app.src.infrastructure.adapters.outbound.persistence.repository.user.initial_admin_repository import UserRepository
from app.src.application.services.initial_admin_service import UserService
from app.src.infrastructure.config.database.database import mongodb



einvoices_router = RouterEInvoices()
users_router = RouterUsers()
report_einvoice_router = RouterReportsEinvoices()
login_router = RouterLogin()



def create_app() -> FastAPI:
    
    
    app = FastAPI(  # Instancia de aplicación FastAPI
        title="BUDGET CLASSIFICATION REST API",
        description="API for operating purchase e-invoices into a finance workspace.",
        version="1.0.0",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,  # Evita expandir los modelos por defecto
            "docExpansion": "none",  # Contrae todas las secciones en Swagger
            # "persistAuthorization": True,  # Permite recordar la autenticación            
        }          
            
    )
    setup_middleware(app)

    app.include_router(einvoices_router.get_router(), prefix="/api")
    app.include_router(users_router.get_router(), prefix="/api")
    app.include_router(report_einvoice_router.get_router(), prefix="/api")
    app.include_router(login_router.get_router(), prefix="/api")
    
    
    
    return app

def setup_middleware(app):
    # Añadir /Configuración de Middlewares
    config_custom_cors_rest = custom_cors_rest()
    config_custom_cors_browser = custom_cors_browser()

        
    app.add_middleware(CustomMiddlewareRest,
                       custom_cors_rest=config_custom_cors_rest)
    app.add_middleware(CustomMiddlewarePreflight,
                       custom_cors_browser=config_custom_cors_browser)
    app.add_middleware(CustomMiddlewareWitoutOrigin)
    
    app.middleware("http")(log_requests) #Logging Middleware

    
app = create_app()

@app.on_event("startup")
async def startup():
    db = mongodb  # Aquí solo necesitas la conexión a la DB
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    await user_service.create_admin_user()  # Verificar o crear el admin al inicio

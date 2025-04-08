from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.requests import Request


# Middleware para permitir solicitudes GET que no tienen por defecto el campo Origin en los Headers HTTP
# para el swagger cuando recargas la página

class CustomMiddlewareWitoutOrigin(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.method == "GET" and not request.headers.get("origin") and not request.headers.get("referer"):
            # Añadir un estado a la solicitud para indicar que no se debe aplicar validación CORS
            request.state.allow_without_origin = True
            return await call_next(request)

        # Si no es GET o tiene Origin, pasa al siguiente middleware
        response = await call_next(request)
        return response

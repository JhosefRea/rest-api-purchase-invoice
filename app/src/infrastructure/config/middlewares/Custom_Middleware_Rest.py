from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from config.cors_config import custom_development_urls
from config.status_code_enum import HTTPStatusEnum

# Middleware para realizar validacioones CORS ESTRICTAS de las solicitudes,
# específicamente mediante los campos Origin o Referer de los HEADERS


class CustomMiddlewareRest(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, custom_cors_rest: dict):
        super().__init__(app)
        self.custom_cors_rest = custom_cors_rest
        self.status_codes = HTTPStatusEnum

    # Interceptor de las peticiones entrantes
    async def dispatch(self, request: Request, call_next):
        self.custom_development_urls = custom_development_urls()

        # Excluir solicitudes de recursos estáticos (favicon, imágenes, etc.)
        if any(static_path in request.url.path for static_path in ["/favicon.ico", "/static/", "/images/"]):
            return await call_next(request)

        # Excluir de los cors y del middleware, rutas de desarrollo
        if request.url.path in self.custom_development_urls:
            return await call_next(request)

        # Si la solicitud fue permitida sin Origin (por CustomMiddlewareWhitoutOrigin), entonces pasar
        if getattr(request.state, "allow_without_origin", False):
            return await call_next(request)

        # Verificar el método HTTP
        if request.method not in self.custom_cors_rest["allow_methods"]:
            return JSONResponse(
                status_code=self.status_codes.METHOD_NOT_ALLOWED.value,
                content={"detail": "Only allowed methods are GET, POST, PUT."},
            )

        # Verificar el encabezado `Origin` o `Referer` de la url en el navegador
        origin = request.headers.get(
            "origin") or request.headers.get("referer")
        print("____origin (URL) que realiza petición ", origin)
        if not origin or origin not in self.custom_cors_rest["allow_origins"]:
            print(f"Request blocked: {
                  'en HEADERS no hay ORIGIN' if not origin else f'ORIGIN no permitido {origin}'}")
            return JSONResponse(
                status_code=self.status_codes.FORBIDDEN.value,
                content={"detail": "Requests from this origin are not allowed"},
            )

        response = await call_next(request)
        return response

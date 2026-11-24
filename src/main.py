"""Sistema de Reporte Ciudadano · punto de entrada.

Aquí solo se arma la aplicación: routers, manejadores de error y el admin inicial.
Capas:  routers (HTTP)  ->  services (reglas)  ->  repositories (datos)
"""
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core import config, security
from src.core.dependencies import get_repo_usuarios
from src.routers import auth, paginas, reportes
from src.services.errores import Conflicto, CredencialesInvalidas, ErrorDominio, NoEncontrado, SinPermiso

app = FastAPI(
    title="Sistema de Reporte Ciudadano",
    version="0.2.0",
    description="API para organizar y dar seguimiento a reportes ciudadanos.",
)


# ==========================================
# SOBRE DE ERROR UNIFORME
# ==========================================

CODIGOS = {
    401: "NO_AUTENTICADO",
    403: "SIN_PERMISO",
    404: "RECURSO_NO_ENCONTRADO",
    405: "METODO_NO_PERMITIDO",
    409: "CONFLICTO",
}


def sobre_error(estado: int, mensaje: str, headers: dict | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=estado,
        headers=headers,
        content={"error": {"codigo": CODIGOS.get(estado, "ERROR_HTTP"), "mensaje": mensaje}},
    )


@app.exception_handler(StarletteHTTPException)
async def manejar_error_http(request, exc):
    # Se conservan los encabezados ("Allow" en un 405, "WWW-Authenticate" en un 401)
    return sobre_error(exc.status_code, str(exc.detail), getattr(exc, "headers", None))


@app.exception_handler(RequestValidationError)
async def manejar_error_validacion(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": {"codigo": "DATOS_INVALIDOS",
                           "mensaje": "Los datos enviados no cumplen con las validaciones."}},
    )


@app.exception_handler(ErrorDominio)
async def manejar_error_dominio(request, exc: ErrorDominio):
    """Traduce los errores de los servicios (que no conocen HTTP) a códigos HTTP."""
    if isinstance(exc, CredencialesInvalidas):
        return sobre_error(401, exc.mensaje, {"WWW-Authenticate": "Bearer"})
    estado = {NoEncontrado: 404, SinPermiso: 403, Conflicto: 409}.get(type(exc), 400)
    return sobre_error(estado, exc.mensaje)


# ==========================================
# RUTAS
# ==========================================

app.include_router(auth.router)
app.include_router(reportes.router)
app.include_router(paginas.router)


@app.get("/health", tags=["sistema"])
def health():
    return {"status": "ok"}


# ==========================================
# ADMINISTRADOR INICIAL (solo si se configura en el entorno)
# ==========================================

def crear_admin_inicial() -> None:
    if not config.ADMIN_PASSWORD:
        return
    repo = get_repo_usuarios()
    if repo.por_nombre(config.ADMIN_USUARIO) is None:
        repo.agregar(config.ADMIN_USUARIO, security.hashear_password(config.ADMIN_PASSWORD), rol="admin")


crear_admin_inicial()

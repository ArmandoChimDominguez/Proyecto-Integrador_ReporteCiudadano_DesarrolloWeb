"""Inyección de dependencias: repositorios, servicios y usuario autenticado.

Los repositorios se crean UNA vez (lru_cache) y se entregan con Depends. En las
pruebas se reemplazan con app.dependency_overrides sin tocar ningún endpoint.
"""
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core import security
from src.models.entidades import Usuario
from src.repositories.memoria import RepositorioTableros, RepositorioTareas, RepositorioUsuarios
from src.services.auth_service import AuthService
from src.services.reportes_service import ReportesService


# ---------- Repositorios (una sola instancia por proceso) ----------
@lru_cache
def get_repo_usuarios() -> RepositorioUsuarios:
    return RepositorioUsuarios()


@lru_cache
def get_repo_tableros() -> RepositorioTableros:
    return RepositorioTableros()


@lru_cache
def get_repo_tareas() -> RepositorioTareas:
    return RepositorioTareas()


# ---------- Servicios ----------
def get_auth_service(
    usuarios: Annotated[RepositorioUsuarios, Depends(get_repo_usuarios)],
) -> AuthService:
    return AuthService(usuarios)


def get_reportes_service(
    tableros: Annotated[RepositorioTableros, Depends(get_repo_tableros)],
    tareas: Annotated[RepositorioTareas, Depends(get_repo_tareas)],
) -> ReportesService:
    return ReportesService(tableros, tareas)


# ---------- Seguridad: autenticación (401) y autorización (403) ----------
bearer = HTTPBearer(auto_error=False)   # sin token -> respondemos 401 nosotros, no 403


def _no_autenticado() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o ausente.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def usuario_actual(
    credenciales: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    usuarios: Annotated[RepositorioUsuarios, Depends(get_repo_usuarios)],
) -> Usuario:
    if credenciales is None:
        raise _no_autenticado()
    try:
        payload = security.decodificar_token(credenciales.credentials)
        usuario = usuarios.por_id(int(payload["sub"]))
    except (security.TokenInvalido, ValueError):
        raise _no_autenticado()
    if usuario is None:                 # el usuario ya no existe
        raise _no_autenticado()
    return usuario                      # el rol se toma del repositorio, no solo del token


def requiere_rol(*roles: str):
    def verificar(usuario: Annotated[Usuario, Depends(usuario_actual)]) -> Usuario:
        if usuario.rol not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "No tienes permiso para este recurso.")
        return usuario
    return verificar


UsuarioActual = Annotated[Usuario, Depends(usuario_actual)]

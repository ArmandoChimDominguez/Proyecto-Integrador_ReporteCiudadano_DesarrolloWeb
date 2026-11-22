"""Rutas de registro, login y perfil."""
from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.core.dependencies import UsuarioActual, get_auth_service
from src.schemas.usuario import Credenciales, Token, UsuarioPublico
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api", tags=["autenticación"])

Auth = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/registro", status_code=status.HTTP_201_CREATED, response_model=UsuarioPublico)
def registro(datos: Credenciales, auth: Auth):
    return auth.registrar(datos.usuario, datos.password)


@router.post("/token", response_model=Token)
def token(datos: Credenciales, auth: Auth):
    access_token, expira = auth.iniciar_sesion(datos.usuario, datos.password)
    return Token(access_token=access_token, expires_in=expira)


@router.get("/perfil", response_model=UsuarioPublico)
def perfil(usuario: UsuarioActual):
    return usuario

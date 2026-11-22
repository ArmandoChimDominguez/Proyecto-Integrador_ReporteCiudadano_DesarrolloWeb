"""Hash de contraseñas (bcrypt) y emisión/validación de JWT. No depende de FastAPI."""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.core import config


class TokenInvalido(Exception):
    """El token está ausente, alterado, vencido o le faltan claims."""


def hashear_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(config.COSTO_BCRYPT)).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


# Hash señuelo: si el usuario no existe se compara contra este, para que el
# login tarde lo mismo y no revele qué usuarios están registrados.
HASH_SENUELO = hashear_password("usuario-inexistente")


def crear_token(usuario_id: int, rol: str) -> str:
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": str(usuario_id),          # el estándar pide que "sub" sea texto
        "rol": rol,
        "iat": ahora,
        "exp": ahora + timedelta(minutes=config.EXPIRA_MINUTOS),
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITMO)


def decodificar_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ALGORITMO],             # nunca aceptar "none" ni otro algoritmo
            options={"require": ["exp", "sub", "rol"]},
        )
    except jwt.InvalidTokenError as exc:              # firma mala, formato roto o vencido
        raise TokenInvalido() from exc

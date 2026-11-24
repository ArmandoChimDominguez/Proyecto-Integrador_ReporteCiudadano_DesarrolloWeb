"""Configuración leída del entorno. Ningún secreto se escribe en el código."""
import os
import secrets

# Si no se define JWT_SECRET_KEY se genera una clave aleatoria al arrancar
# (útil en desarrollo; los tokens dejan de servir al reiniciar el servidor).
SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY") or secrets.token_urlsafe(48)
ALGORITMO: str = "HS256"
EXPIRA_MINUTOS: int = int(os.environ.get("JWT_EXPIRA_MINUTOS", "30"))
COSTO_BCRYPT: int = int(os.environ.get("BCRYPT_COSTO", "12"))

# Administrador inicial: solo se crea si se define ADMIN_PASSWORD en el entorno.
ADMIN_USUARIO: str = os.environ.get("ADMIN_USUARIO", "admin")
ADMIN_PASSWORD: str | None = os.environ.get("ADMIN_PASSWORD")

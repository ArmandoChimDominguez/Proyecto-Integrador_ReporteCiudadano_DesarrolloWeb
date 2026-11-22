"""Reglas de registro e inicio de sesión."""
from src.core import config, security
from src.models.entidades import Usuario
from src.repositories.memoria import RepositorioUsuarios
from src.services.errores import Conflicto, CredencialesInvalidas


class AuthService:
    def __init__(self, usuarios: RepositorioUsuarios) -> None:
        self.usuarios = usuarios

    def registrar(self, usuario: str, password: str) -> Usuario:
        if self.usuarios.por_nombre(usuario) is not None:
            raise Conflicto("El usuario ya existe.")
        # El rol NUNCA lo decide el cliente: todo registro nuevo es "user"
        return self.usuarios.agregar(usuario, security.hashear_password(password), rol="user")

    def iniciar_sesion(self, usuario: str, password: str) -> tuple[str, int]:
        encontrado = self.usuarios.por_nombre(usuario)
        hash_a_comparar = encontrado.password_hash if encontrado else security.HASH_SENUELO
        valido = security.verificar_password(password, hash_a_comparar)
        if encontrado is None or not valido:
            raise CredencialesInvalidas("Usuario o contraseña incorrectos.")
        return security.crear_token(encontrado.id, encontrado.rol), config.EXPIRA_MINUTOS * 60

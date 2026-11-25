"""DTOs de autenticación. La contraseña solo existe en las entradas."""
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Credenciales(BaseModel):
    model_config = ConfigDict(extra="forbid")

    usuario: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str = Field(min_length=6)

    @field_validator("password")
    @classmethod
    def limite_bcrypt(cls, valor: str) -> str:
        # bcrypt solo usa los primeros 72 BYTES; se rechaza en lugar de cortar en silencio
        if len(valor.encode("utf-8")) > 72:
            raise ValueError("la contraseña no puede exceder 72 bytes")
        return valor


class UsuarioPublico(BaseModel):
    """Lo único que sale de la API sobre un usuario: nunca la contraseña ni el hash."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario: str
    rol: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

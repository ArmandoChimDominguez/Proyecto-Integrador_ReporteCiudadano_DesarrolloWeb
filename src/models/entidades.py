"""Entidades internas del dominio. Lo que se guarda, no lo que se muestra."""
from dataclasses import dataclass


@dataclass
class Usuario:
    id: int
    usuario: str
    password_hash: str
    rol: str = "user"        # "user" | "admin"


@dataclass
class Tablero:
    id: int
    nombre: str
    descripcion: str | None
    usuario_id: int          # dueño del tablero


@dataclass
class Tarea:
    id: int
    tablero_id: int
    titulo: str
    descripcion: str
    categoria: str
    ubicacion: str
    estado: str = "pendiente"

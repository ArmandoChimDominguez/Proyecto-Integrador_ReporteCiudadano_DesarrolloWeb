"""Repositorios en memoria. No importan FastAPI: solo guardan y buscan entidades.

En el Hito 3 se reemplazan por repositorios con SQLAlchemy que tengan los mismos
métodos; los servicios y routers no tendrán que cambia.
"""
from dataclasses import replace

from src.models.entidades import Tablero, Tarea, Usuario


class RepositorioUsuarios:
    def __init__(self) -> None:
        self._datos: dict[int, Usuario] = {}
        self._siguiente = 1

    def agregar(self, usuario: str, password_hash: str, rol: str = "user") -> Usuario:
        nuevo = Usuario(id=self._siguiente, usuario=usuario, password_hash=password_hash, rol=rol)
        self._datos[nuevo.id] = nuevo
        self._siguiente += 1
        return replace(nuevo)

    def por_id(self, usuario_id: int) -> Usuario | None:
        encontrado = self._datos.get(usuario_id)
        return replace(encontrado) if encontrado else None

    def por_nombre(self, usuario: str) -> Usuario | None:
        for u in self._datos.values():
            if u.usuario == usuario:
                return replace(u)
        return None


class RepositorioTableros:
    def __init__(self) -> None:
        self._datos: dict[int, Tablero] = {}
        self._siguiente = 1

    def agregar(self, nombre: str, descripcion: str | None, usuario_id: int) -> Tablero:
        nuevo = Tablero(id=self._siguiente, nombre=nombre, descripcion=descripcion, usuario_id=usuario_id)
        self._datos[nuevo.id] = nuevo
        self._siguiente += 1
        return replace(nuevo)

    def por_id(self, tablero_id: int) -> Tablero | None:
        encontrado = self._datos.get(tablero_id)
        return replace(encontrado) if encontrado else None

    def listar(self, usuario_id: int | None = None) -> list[Tablero]:
        """Sin usuario_id devuelve todos (uso de administrador)."""
        return [replace(t) for t in self._datos.values()
                if usuario_id is None or t.usuario_id == usuario_id]


class RepositorioTareas:
    def __init__(self) -> None:
        self._datos: dict[int, Tarea] = {}
        self._siguiente = 1

    def agregar(self, tablero_id: int, **campos) -> Tarea:
        nueva = Tarea(id=self._siguiente, tablero_id=tablero_id, **campos)
        self._datos[nueva.id] = nueva
        self._siguiente += 1
        return replace(nueva)

    def por_id(self, tarea_id: int) -> Tarea | None:
        encontrada = self._datos.get(tarea_id)
        return replace(encontrada) if encontrada else None

    def listar_por_tablero(self, tablero_id: int) -> list[Tarea]:
        return [replace(t) for t in self._datos.values() if t.tablero_id == tablero_id]

    def eliminar(self, tarea_id: int) -> bool:
        return self._datos.pop(tarea_id, None) is not None

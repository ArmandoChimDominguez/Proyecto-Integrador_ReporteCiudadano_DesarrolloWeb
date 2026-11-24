"""Reglas de negocio de tableros (zonas) y tareas (reportes), incluida la propiedad."""
from src.models.entidades import Tablero, Tarea, Usuario
from src.repositories.memoria import RepositorioTableros, RepositorioTareas
from src.services.errores import NoEncontrado, SinPermiso


class ReportesService:
    def __init__(self, tableros: RepositorioTableros, tareas: RepositorioTareas) -> None:
        self.tableros = tableros
        self.tareas = tareas

    # ---- reglas de acceso ----
    @staticmethod
    def _puede_usar(usuario: Usuario, tablero: Tablero) -> bool:
        return usuario.rol == "admin" or tablero.usuario_id == usuario.id

    def _tablero_permitido(self, tablero_id: int, usuario: Usuario) -> Tablero:
        tablero = self.tableros.por_id(tablero_id)
        if tablero is None:
            raise NoEncontrado("El tablero solicitado no existe.")
        if not self._puede_usar(usuario, tablero):
            raise SinPermiso("No tienes permiso sobre este tablero.")
        return tablero

    # ---- tableros ----
    def crear_tablero(self, nombre: str, descripcion: str | None, usuario: Usuario) -> Tablero:
        return self.tableros.agregar(nombre, descripcion, usuario.id)

    def listar_tableros(self, usuario: Usuario) -> list[Tablero]:
        # Un user ve solo los suyos; un admin ve todos
        return self.tableros.listar(None if usuario.rol == "admin" else usuario.id)

    # ---- tareas ----
    def crear_tarea(self, tablero_id: int, datos: dict, usuario: Usuario) -> Tarea:
        self._tablero_permitido(tablero_id, usuario)
        return self.tareas.agregar(tablero_id, **datos)

    def listar_tareas(self, tablero_id: int, usuario: Usuario) -> list[Tarea]:
        self._tablero_permitido(tablero_id, usuario)
        return self.tareas.listar_por_tablero(tablero_id)

    def consultar_tarea(self, tarea_id: int, usuario: Usuario) -> Tarea:
        tarea = self.tareas.por_id(tarea_id)
        if tarea is None:
            raise NoEncontrado("La tarea solicitada no existe.")
        self._tablero_permitido(tarea.tablero_id, usuario)
        return tarea

    def eliminar_tarea(self, tarea_id: int, usuario: Usuario) -> None:
        tarea = self.consultar_tarea(tarea_id, usuario)   # 404 si no existe, 403 si no es dueño
        self.tareas.eliminar(tarea.id)

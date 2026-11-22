"""Rutas HTTP de tableros y tareas. Solo validan el contrato y delegan al servicio."""
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from src.core.dependencies import UsuarioActual, get_reportes_service
from src.schemas.tablero import ListaTableros, TableroCreate, TableroResponse
from src.schemas.tarea import ListaTareas, TareaCreate, TareaResponse
from src.services.reportes_service import ReportesService

router = APIRouter(prefix="/api", tags=["reportes"])

Servicio = Annotated[ReportesService, Depends(get_reportes_service)]


@router.post("/tableros", response_model=TableroResponse, status_code=status.HTTP_201_CREATED)
def crear_tablero(datos: TableroCreate, usuario: UsuarioActual, servicio: Servicio):
    return servicio.crear_tablero(datos.nombre, datos.descripcion, usuario)


@router.get("/tableros", response_model=ListaTableros)
def listar_tableros(usuario: UsuarioActual, servicio: Servicio):
    return {"tableros": servicio.listar_tableros(usuario)}


@router.post("/tableros/{tablero_id}/tareas", response_model=TareaResponse,
             status_code=status.HTTP_201_CREATED)
def crear_tarea(tablero_id: int, datos: TareaCreate, usuario: UsuarioActual, servicio: Servicio):
    return servicio.crear_tarea(tablero_id, datos.model_dump(), usuario)


@router.get("/tableros/{tablero_id}/tareas", response_model=ListaTareas)
def listar_tareas(tablero_id: int, usuario: UsuarioActual, servicio: Servicio):
    return {"tareas": servicio.listar_tareas(tablero_id, usuario)}


@router.get("/tareas/{tarea_id}", response_model=TareaResponse)
def consultar_tarea(tarea_id: int, usuario: UsuarioActual, servicio: Servicio):
    return servicio.consultar_tarea(tarea_id, usuario)


@router.delete("/tareas/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(tarea_id: int, usuario: UsuarioActual, servicio: Servicio):
    servicio.eliminar_tarea(tarea_id, usuario)
    return Response(status_code=status.HTTP_204_NO_CONTENT)   # 204: sin cuerpo

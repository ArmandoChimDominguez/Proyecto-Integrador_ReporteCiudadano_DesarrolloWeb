from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TareaCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str = Field(min_length=5, max_length=100)
    descripcion: str = Field(min_length=10, max_length=500)
    categoria: Literal["baches", "alumbrado", "basura"]
    ubicacion: str = Field(min_length=5, max_length=150)
    estado: Literal["pendiente", "en_progreso", "resuelta"] = "pendiente"


class TareaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tablero_id: int
    titulo: str
    descripcion: str
    categoria: str
    ubicacion: str
    estado: str


class ListaTareas(BaseModel):
    tareas: list[TareaResponse]

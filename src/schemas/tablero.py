from pydantic import BaseModel, ConfigDict, Field


class TableroCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: str = Field(min_length=3, max_length=60)
    descripcion: str | None = Field(default=None, max_length=250)


class TableroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
    usuario_id: int


class ListaTableros(BaseModel):
    tableros: list[TableroResponse]

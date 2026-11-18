
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel, Field


# ==========================================
# CONFIGURACION DE LA APLICACION
# ==========================================

app = FastAPI(
    title="Sistema de Reporte Ciudadano",
    version="0.1.0",
    description="API para organizar y dar seguimiento a reportes ciudadanos."
)

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ==========================================
# MODELOS DTO: TABLEROS
# ==========================================

class TableroCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=60)
    descripcion: str | None = Field(default=None, max_length=250)


class TableroResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    usuario_id: int


# ==========================================
# MODELOS DTO: TAREAS
# ==========================================

class TareaCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=100)
    descripcion: str = Field(min_length=10, max_length=500)
    categoria: Literal["baches", "alumbrado", "basura"]
    ubicacion: str = Field(min_length=5, max_length=150)
    estado: Literal["pendiente", "en_progreso", "resuelta"] = "pendiente"


class TareaResponse(BaseModel):
    id: int
    tablero_id: int
    titulo: str
    descripcion: str
    categoria: str
    ubicacion: str
    estado: str


class ListaTableros(BaseModel):
    tableros: list[TableroResponse]


class ListaTareas(BaseModel):
    tareas: list[TareaResponse]


# ==========================================
# ALMACENAMIENTO TEMPORAL
# ==========================================

tableros = {}
tareas = {}

contador_tableros = 1
contador_tareas = 1

USUARIO_ID = 1


# ==========================================
# MANEJO DE ERRORES
# ==========================================

@app.exception_handler(StarletteHTTPException)
async def manejar_error_http(request, exc):
    codigos = {404: "RECURSO_NO_ENCONTRADO", 405: "METODO_NO_PERMITIDO"}
    return JSONResponse(
        status_code=exc.status_code,
        # Se conservan los encabezados (por ejemplo "Allow" en un 405)
        headers=getattr(exc, "headers", None),
        content={
            "error": {
                "codigo": codigos.get(exc.status_code, "ERROR_HTTP"),
                "mensaje": str(exc.detail)
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def manejar_error_validacion(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "codigo": "DATOS_INVALIDOS",
                "mensaje": "Los datos enviados no cumplen con las validaciones."
            }
        }
    )


# ==========================================
# RUTAS DEL SITIO CIUDADANO
# ==========================================

@app.get("/", include_in_schema=False)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="SITIO/index.html",
        context={}
    )


@app.get("/reportar", include_in_schema=False)
async def pagina_reportar(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="SITIO/reportar.html",
        context={}
    )


@app.get("/mis-reportes", include_in_schema=False)
async def mis_reportes(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="SITIO/mis_reportes.html",
        context={}
    )


@app.get("/detalle-reporte", include_in_schema=False)
async def detalle_reporte(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="SITIO/detalle_reporte.html",
        context={}
    )


@app.get("/contacto", include_in_schema=False)
async def contacto(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="SITIO/contacto.html",
        context={}
    )


# ==========================================
# RUTAS DEL PANEL ADMINISTRATIVO
# ==========================================

@app.get("/admin", include_in_schema=False)
async def login_admin(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="ADMIN/login.html",
        context={}
    )


@app.get("/admin/dashboard", include_in_schema=False)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="ADMIN/dashboard.html",
        context={}
    )


@app.get("/admin/reportes", include_in_schema=False)
async def administrar_reportes(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="ADMIN/reportes.html",
        context={}
    )


@app.get("/admin/reporte-nuevo", include_in_schema=False)
async def nuevo_reporte(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="ADMIN/reporte_nuevo.html",
        context={}
    )


@app.get("/admin/reporte-editar", include_in_schema=False)
async def editar_reporte(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="ADMIN/reporte_editar.html",
        context={}
    )


# ==========================================
# ENDPOINT: VERIFICAR SERVIDOR
# ==========================================

@app.get("/health")
def health():
    return {"status": "ok"}


# ==========================================
# ENDPOINTS: TABLEROS
# ==========================================

@app.post(
    "/api/tableros",
    response_model=TableroResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_tablero(datos: TableroCreate):

    global contador_tableros

    nuevo_tablero = {
        "id": contador_tableros,
        "nombre": datos.nombre,
        "descripcion": datos.descripcion,
        "usuario_id": USUARIO_ID
    }

    tableros[contador_tableros] = nuevo_tablero
    contador_tableros += 1

    return nuevo_tablero


@app.get("/api/tableros", response_model=ListaTableros)
def listar_tableros():
    # Hito 1: usuario fijo; solo se listan los tableros de ese usuario
    return {
        "tableros": [
            tablero for tablero in tableros.values()
            if tablero["usuario_id"] == USUARIO_ID
        ]
    }


# ==========================================
# ENDPOINTS: TAREAS
# ==========================================

@app.post(
    "/api/tableros/{tablero_id}/tareas",
    response_model=TareaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_tarea(tablero_id: int, datos: TareaCreate):

    global contador_tareas

    if tablero_id not in tableros:
        raise HTTPException(
            status_code=404,
            detail="El tablero solicitado no existe."
        )

    nueva_tarea = {
        "id": contador_tareas,
        "tablero_id": tablero_id,
        "titulo": datos.titulo,
        "descripcion": datos.descripcion,
        "categoria": datos.categoria,
        "ubicacion": datos.ubicacion,
        "estado": datos.estado
    }

    tareas[contador_tareas] = nueva_tarea
    contador_tareas += 1

    return nueva_tarea


@app.get("/api/tableros/{tablero_id}/tareas", response_model=ListaTareas)
def listar_tareas(tablero_id: int):

    if tablero_id not in tableros:
        raise HTTPException(
            status_code=404,
            detail="El tablero solicitado no existe."
        )

    return {
        "tareas": [
            tarea for tarea in tareas.values()
            if tarea["tablero_id"] == tablero_id
        ]
    }


@app.get("/api/tareas/{tarea_id}", response_model=TareaResponse)
def consultar_tarea(tarea_id: int):

    if tarea_id not in tareas:
        raise HTTPException(
            status_code=404,
            detail="La tarea solicitada no existe."
        )

    return tareas[tarea_id]


@app.delete("/api/tareas/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(tarea_id: int):

    if tarea_id not in tareas:
        raise HTTPException(
            status_code=404,
            detail="La tarea solicitada no existe."
        )

    del tareas[tarea_id]

    # 204 No Content: la eliminación fue exitosa y no hay cuerpo
    return Response(status_code=status.HTTP_204_NO_CONTENT)

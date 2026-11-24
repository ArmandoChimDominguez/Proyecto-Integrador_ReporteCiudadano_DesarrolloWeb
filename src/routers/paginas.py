"""Páginas HTML del sitio ciudadano y del panel (vistas del proyecto original)."""
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(include_in_schema=False)

# ruta -> plantilla
PAGINAS = {
    "/": "SITIO/index.html",
    "/reportar": "SITIO/reportar.html",
    "/mis-reportes": "SITIO/mis_reportes.html",
    "/detalle-reporte": "SITIO/detalle_reporte.html",
    "/contacto": "SITIO/contacto.html",
    "/admin": "ADMIN/login.html",
    "/admin/dashboard": "ADMIN/dashboard.html",
    "/admin/reportes": "ADMIN/reportes.html",
    "/admin/reporte-nuevo": "ADMIN/reporte_nuevo.html",
    "/admin/reporte-editar": "ADMIN/reporte_editar.html",
}


def _vista(plantilla: str):
    async def mostrar(request: Request):
        return templates.TemplateResponse(request=request, name=plantilla, context={})
    return mostrar


for ruta, plantilla in PAGINAS.items():
    router.add_api_route(ruta, _vista(plantilla), methods=["GET"])

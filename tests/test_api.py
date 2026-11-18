"""Pruebas del Hito 1 · Sistema de Reporte Ciudadano.

Ejecutar desde la raíz del repositorio:

    pytest -q

Cada prueba revisa el código HTTP **y** el cuerpo de la respuesta.
"""
import pytest
from fastapi.testclient import TestClient

from src import main
from src.main import app

client = TestClient(app)

TABLERO_VALIDO = {"nombre": "Colonia Centro", "descripcion": "Reportes de la zona centro"}
TAREA_VALIDA = {
    "titulo": "Bache en avenida principal",
    "descripcion": "Bache profundo frente al parque, riesgo para motociclistas.",
    "categoria": "baches",
    "ubicacion": "Av. Javier Rojo Gómez esq. calle 5",
}


@pytest.fixture(autouse=True)
def datos_limpios():
    """Cada prueba arranca con el almacenamiento en memoria vacío."""
    main.tableros.clear()
    main.tareas.clear()
    main.contador_tableros = 1
    main.contador_tareas = 1
    yield


def crear_tablero() -> dict:
    respuesta = client.post("/api/tableros", json=TABLERO_VALIDO)
    assert respuesta.status_code == 201
    return respuesta.json()


# 1. Crear principal válido -> 201 con id
def test_crear_tablero_valido():
    respuesta = client.post("/api/tableros", json=TABLERO_VALIDO)
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Colonia Centro"
    assert cuerpo["usuario_id"] == 1


# 2. Crear principal con campo inválido -> 422 con sobre de error
def test_crear_tablero_invalido():
    respuesta = client.post("/api/tableros", json={"nombre": "AB"})  # menos de 3 caracteres
    assert respuesta.status_code == 422
    assert respuesta.json()["error"]["codigo"] == "DATOS_INVALIDOS"


# 3. Listar principales -> 200 con lista envuelta
def test_listar_tableros():
    crear_tablero()
    respuesta = client.get("/api/tableros")
    assert respuesta.status_code == 200
    tableros = respuesta.json()["tableros"]
    assert len(tableros) == 1
    assert tableros[0]["nombre"] == "Colonia Centro"


# 4. Crear hijo válido -> 201
def test_crear_tarea_valida():
    tablero = crear_tablero()
    respuesta = client.post(f"/api/tableros/{tablero['id']}/tareas", json=TAREA_VALIDA)
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["id"] == 1
    assert cuerpo["tablero_id"] == tablero["id"]
    assert cuerpo["estado"] == "pendiente"  # valor por defecto


# 5. Crear hijo en padre inexistente -> 404 con sobre de error
def test_crear_tarea_en_tablero_inexistente():
    respuesta = client.post("/api/tableros/999/tareas", json=TAREA_VALIDA)
    assert respuesta.status_code == 404
    assert respuesta.json()["error"]["codigo"] == "RECURSO_NO_ENCONTRADO"


# 6. Listar hijos del padre -> 200 con lista
def test_listar_tareas_del_tablero():
    tablero = crear_tablero()
    client.post(f"/api/tableros/{tablero['id']}/tareas", json=TAREA_VALIDA)
    respuesta = client.get(f"/api/tableros/{tablero['id']}/tareas")
    assert respuesta.status_code == 200
    tareas = respuesta.json()["tareas"]
    assert len(tareas) == 1
    assert tareas[0]["categoria"] == "baches"


# 7. Eliminar hijo y consultarlo -> 204 y luego 404
def test_eliminar_tarea_y_consultarla():
    tablero = crear_tablero()
    tarea = client.post(f"/api/tableros/{tablero['id']}/tareas", json=TAREA_VALIDA).json()

    borrado = client.delete(f"/api/tareas/{tarea['id']}")
    assert borrado.status_code == 204
    assert borrado.content == b""  # 204 no lleva cuerpo

    consulta = client.get(f"/api/tareas/{tarea['id']}")
    assert consulta.status_code == 404
    assert consulta.json()["error"]["codigo"] == "RECURSO_NO_ENCONTRADO"


# 8. Verbo no permitido -> 405 (no 404)
def test_verbo_no_permitido():
    respuesta = client.patch("/api/tareas/1", json={"estado": "resuelta"})
    assert respuesta.status_code == 405
    assert respuesta.json()["error"]["codigo"] == "METODO_NO_PERMITIDO"
    assert "allow" in respuesta.headers

"""Pruebas del contrato del Hito 1, ahora con autenticación (Hito 2).

Ejecutar desde la raíz del repositorio:

    pytest -q
"""
import pytest

from tests.conftest import token_de

TABLERO_VALIDO = {"nombre": "Colonia Centro", "descripcion": "Reportes de la zona centro"}
TAREA_VALIDA = {
    "titulo": "Bache en avenida principal",
    "descripcion": "Bache profundo frente al parque, riesgo para motociclistas.",
    "categoria": "baches",
    "ubicacion": "Av. Javier Rojo Gómez esq. calle 5",
}


@pytest.fixture
def ana(client):
    return token_de(client, "ana")


def crear_tablero(client, headers) -> dict:
    respuesta = client.post("/api/tableros", json=TABLERO_VALIDO, headers=headers)
    assert respuesta.status_code == 201
    return respuesta.json()


# 1. Crear principal válido -> 201 con id y dueño
def test_crear_tablero_valido(client, ana):
    respuesta = client.post("/api/tableros", json=TABLERO_VALIDO, headers=ana)
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Colonia Centro"
    assert cuerpo["usuario_id"] == client.get("/api/perfil", headers=ana).json()["id"]


# 2. Crear principal con campo inválido -> 422 con sobre de error
def test_crear_tablero_invalido(client, ana):
    respuesta = client.post("/api/tableros", json={"nombre": "AB"}, headers=ana)
    assert respuesta.status_code == 422
    assert respuesta.json()["error"]["codigo"] == "DATOS_INVALIDOS"


# 3. Listar principales -> 200 con lista envuelta
def test_listar_tableros(client, ana):
    crear_tablero(client, ana)
    respuesta = client.get("/api/tableros", headers=ana)
    assert respuesta.status_code == 200
    tableros = respuesta.json()["tableros"]
    assert len(tableros) == 1
    assert tableros[0]["nombre"] == "Colonia Centro"


# 4. Crear hijo válido -> 201
def test_crear_tarea_valida(client, ana):
    tablero = crear_tablero(client, ana)
    respuesta = client.post(f"/api/tableros/{tablero['id']}/tareas", json=TAREA_VALIDA, headers=ana)
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["id"] == 1
    assert cuerpo["tablero_id"] == tablero["id"]
    assert cuerpo["estado"] == "pendiente"  # valor por defecto


# 5. Crear hijo en padre inexistente -> 404 con sobre de error
def test_crear_tarea_en_tablero_inexistente(client, ana):
    respuesta = client.post("/api/tableros/999/tareas", json=TAREA_VALIDA, headers=ana)
    assert respuesta.status_code == 404
    assert respuesta.json()["error"]["codigo"] == "RECURSO_NO_ENCONTRADO"


# 6. Listar hijos del padre -> 200 con lista
def test_listar_tareas_del_tablero(client, ana):
    tablero = crear_tablero(client, ana)
    client.post(f"/api/tableros/{tablero['id']}/tareas", json=TAREA_VALIDA, headers=ana)
    respuesta = client.get(f"/api/tableros/{tablero['id']}/tareas", headers=ana)
    assert respuesta.status_code == 200
    tareas = respuesta.json()["tareas"]
    assert len(tareas) == 1
    assert tareas[0]["categoria"] == "baches"


# 7. Eliminar hijo y consultarlo -> 204 y luego 404
def test_eliminar_tarea_y_consultarla(client, ana):
    tablero = crear_tablero(client, ana)
    tarea = client.post(f"/api/tableros/{tablero['id']}/tareas", json=TAREA_VALIDA, headers=ana).json()

    borrado = client.delete(f"/api/tareas/{tarea['id']}", headers=ana)
    assert borrado.status_code == 204
    assert borrado.content == b""  # 204 no lleva cuerpo

    consulta = client.get(f"/api/tareas/{tarea['id']}", headers=ana)
    assert consulta.status_code == 404
    assert consulta.json()["error"]["codigo"] == "RECURSO_NO_ENCONTRADO"


# 8. Verbo no permitido -> 405 (no 404) y encabezado Allow
def test_verbo_no_permitido(client):
    respuesta = client.patch("/api/tareas/1", json={"estado": "resuelta"})
    assert respuesta.status_code == 405
    assert respuesta.json()["error"]["codigo"] == "METODO_NO_PERMITIDO"
    assert "allow" in respuesta.headers

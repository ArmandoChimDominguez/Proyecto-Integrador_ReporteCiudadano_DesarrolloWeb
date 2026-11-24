"""Configuración común de las pruebas

Cada prueba recibe repositorios NUEVOS gracias a app.dependency_overrides:
así se demuestra que la inyección de dependencias permite sustituir la capa de
datos sin modificar ningún endpoint.
"""
import os

os.environ.setdefault("BCRYPT_COSTO", "4")          # hash más rápido solo en pruebas
os.environ.setdefault("JWT_SECRET_KEY", "clave-solo-para-pruebas-no-usar-en-produccion")

import pytest
from fastapi.testclient import TestClient

from src.core import dependencies, security
from src.main import app
from src.repositories.memoria import RepositorioTableros, RepositorioTareas, RepositorioUsuarios

ADMIN = {"usuario": "admin", "password": "admin-pruebas"}


@pytest.fixture
def client():
    usuarios, tableros, tareas = RepositorioUsuarios(), RepositorioTableros(), RepositorioTareas()
    usuarios.agregar(ADMIN["usuario"], security.hashear_password(ADMIN["password"]), rol="admin")

    app.dependency_overrides[dependencies.get_repo_usuarios] = lambda: usuarios
    app.dependency_overrides[dependencies.get_repo_tableros] = lambda: tableros
    app.dependency_overrides[dependencies.get_repo_tareas] = lambda: tareas
    yield TestClient(app)
    app.dependency_overrides.clear()


def token_de(client: TestClient, usuario: str, password: str = "secreta123", registrar: bool = True) -> dict:
    """Registra (opcional), inicia sesión y devuelve el encabezado Authorization."""
    if registrar:
        assert client.post("/api/registro", json={"usuario": usuario, "password": password}).status_code == 201
    respuesta = client.post("/api/token", json={"usuario": usuario, "password": password})
    assert respuesta.status_code == 200
    return {"Authorization": f"Bearer {respuesta.json()['access_token']}"}

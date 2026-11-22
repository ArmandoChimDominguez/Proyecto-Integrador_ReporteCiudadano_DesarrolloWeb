"""Las diez pruebas del Hito 2: registro, login, 401/403 y roles."""
from tests.conftest import ADMIN, token_de

TABLERO = {"nombre": "Colonia Centro"}
TAREA = {
    "titulo": "Lámpara fundida",
    "descripcion": "La lámpara de la esquina no enciende desde hace una semana.",
    "categoria": "alumbrado",
    "ubicacion": "Calle 22 entre 59 y 61",
}


def tarea_de(client, headers) -> dict:
    tablero = client.post("/api/tableros", json=TABLERO, headers=headers).json()
    return client.post(f"/api/tableros/{tablero['id']}/tareas", json=TAREA, headers=headers).json()


# 1. Registro válido -> 201 sin contraseña ni hash
def test_01_registro_valido(client):
    respuesta = client.post("/api/registro", json={"usuario": "ana", "password": "secreta123"})
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["usuario"] == "ana" and cuerpo["rol"] == "user"
    assert "password" not in cuerpo and "password_hash" not in cuerpo
    assert "secreta123" not in respuesta.text


# 2. Registro duplicado -> 409
def test_02_registro_duplicado(client):
    datos = {"usuario": "ana", "password": "secreta123"}
    client.post("/api/registro", json=datos)
    respuesta = client.post("/api/registro", json=datos)
    assert respuesta.status_code == 409
    assert respuesta.json()["error"]["codigo"] == "CONFLICTO"


# 3. Login correcto -> 200 + token
def test_03_login_correcto(client):
    client.post("/api/registro", json={"usuario": "ana", "password": "secreta123"})
    respuesta = client.post("/api/token", json={"usuario": "ana", "password": "secreta123"})
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["access_token"] and cuerpo["token_type"] == "bearer"


# 4. Login incorrecto -> 401
def test_04_login_incorrecto(client):
    client.post("/api/registro", json={"usuario": "ana", "password": "secreta123"})
    respuesta = client.post("/api/token", json={"usuario": "ana", "password": "otra-clave"})
    assert respuesta.status_code == 401
    assert respuesta.json()["error"]["codigo"] == "NO_AUTENTICADO"


# 5. Ruta protegida con token -> 200
def test_05_perfil_con_token(client):
    headers = token_de(client, "ana")
    respuesta = client.get("/api/perfil", headers=headers)
    assert respuesta.status_code == 200
    assert respuesta.json()["usuario"] == "ana"


# 6. Ruta protegida sin token -> 401 (no 403)
def test_06_sin_token(client):
    respuesta = client.get("/api/tableros")
    assert respuesta.status_code == 401
    assert respuesta.headers["www-authenticate"] == "Bearer"


# 7. Token alterado -> 401 (nunca 500)
def test_07_token_alterado(client):
    headers = token_de(client, "ana")
    headers["Authorization"] += "x"
    respuesta = client.get("/api/tableros", headers=headers)
    assert respuesta.status_code == 401


# 8. El dueño elimina su tarea -> 204
def test_08_duenio_elimina(client):
    ana = token_de(client, "ana")
    tarea = tarea_de(client, ana)
    assert client.delete(f"/api/tareas/{tarea['id']}", headers=ana).status_code == 204


# 9. Otro usuario intenta eliminar -> 403 y la tarea sigue existiendo
def test_09_otro_usuario_no_elimina(client):
    ana, luis = token_de(client, "ana"), token_de(client, "luis")
    tarea = tarea_de(client, ana)
    respuesta = client.delete(f"/api/tareas/{tarea['id']}", headers=luis)
    assert respuesta.status_code == 403
    assert respuesta.json()["error"]["codigo"] == "SIN_PERMISO"
    assert client.get(f"/api/tareas/{tarea['id']}", headers=ana).status_code == 200


# 10. El admin lista todos; cada usuario solo los suyos
def test_10_admin_lista_todos(client):
    ana, luis = token_de(client, "ana"), token_de(client, "luis")
    client.post("/api/tableros", json={"nombre": "Zona de Ana"}, headers=ana)
    client.post("/api/tableros", json={"nombre": "Zona de Luis"}, headers=luis)
    admin = token_de(client, ADMIN["usuario"], ADMIN["password"], registrar=False)

    todos = client.get("/api/tableros", headers=admin)
    assert todos.status_code == 200
    assert len(todos.json()["tableros"]) == 2
    solo_ana = client.get("/api/tableros", headers=ana).json()["tableros"]
    assert [t["nombre"] for t in solo_ana] == ["Zona de Ana"]

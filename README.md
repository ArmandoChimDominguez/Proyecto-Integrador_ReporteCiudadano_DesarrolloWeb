# Proyecto Integrador · Sistema de Reporte Ciudadano

**Curso:** Desarrollo de Aplicaciones Web (DAB-2201) · TecNM Cancún  
**Equipo:** Pedro Pablo Pool Ché (`XxZoroxX10`) y `BrokeniGS` (L23531079)  
**Dominio:** Tablero → Tarea, adaptado a reportes ciudadanos (pendiente de confirmar con el docente)  
**Repositorio:** https://github.com/XxZoroxX10/Proyecto-Integrador_ReporteCiudadano_DesarrolloWeb  
**Docente:** MCC. Iván Márquez Larios (`ijmarquezl`)

---

## 1. ¿Qué resuelve?

Los vecinos reportan problemas de su colonia (baches, alumbrado, basura) y les dan seguimiento hasta que se resuelven. Cada **tablero** agrupa los reportes de una zona y cada **tarea** es un reporte con categoría, ubicación y estado.

## 2. Alcance

- Entidad principal: `Tablero` (zona o colonia).
- Entidad secundaria: `Tarea` (reporte ciudadano), relación 1:N.
- Usuario: registro, login y rol `user`/`admin` (Hito 2).
- Interfaz: una SPA con login, lista, formulario y eliminar (Hito 4).
- Fuera de alcance: subir fotos, mapas, notificaciones y APIs externas.

## 3. Stack

- Backend: FastAPI + Pydantic v2
- Base de datos: en memoria (Hito 1); SQLite desde el Hito 3
- ORM / migraciones: SQLAlchemy + Alembic (Hito 3)
- Frontend: HTML, CSS y JavaScript vanilla
- Pruebas: pytest + TestClient (httpx)

## 4. Cómo ejecutarlo

```bash
python -m venv .venv
source .venv/bin/activate       # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

Abre `http://127.0.0.1:8000/docs`.

### Pruebas

```bash
pytest -q
```

Resultado actual: **8 passed**.

## 5. Endpoints (Hito 1, usuario fijo `usuario_id = 1`)

| Método | Ruta | Qué hace | Respuesta |
| :--- | :--- | :--- | :--- |
| GET | `/health` | Estado del servicio | 200 `{"status":"ok"}` |
| GET | `/api/tableros` | Lista los tableros del usuario | 200 `{"tableros":[...]}` |
| POST | `/api/tableros` | Crea un tablero | 201 con `id` / 422 |
| GET | `/api/tableros/{id}/tareas` | Lista los reportes del tablero | 200 `{"tareas":[...]}` / 404 |
| POST | `/api/tableros/{id}/tareas` | Crea un reporte | 201 / 404 / 422 |
| GET | `/api/tareas/{id}` | Consulta un reporte | 200 / 404 |
| DELETE | `/api/tareas/{id}` | Elimina un reporte | 204 / 404 |

Errores con sobre uniforme: `{"error": {"codigo": "...", "mensaje": "..."}}`.

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/tableros/1/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Bache en avenida principal","descripcion":"Bache profundo frente al parque","categoria":"baches","ubicacion":"Av. Rojo Gómez esq. calle 5"}'
# 201 {"id":1,"tablero_id":1,...,"estado":"pendiente"}
```

## 6. Hitos y etiquetas

| Hito | Sesión | Tag | Estado |
| :--- | :---: | :--- | :--- |
| 1. Contrato y mock | 10 | `v0.1-hito1` | [x] Código y 8 pruebas |
| 2. Capas y seguridad | 20 | `v0.2-hito2` | [ ] |
| 3. Persistencia y OWASP | 30 | `v0.3-hito3` | [ ] |
| 4. Producto | 40 | `v1.0-final` | [ ] |

## 7. Documentos

- [Propuesta](docs/propuesta.md)
- [Acuerdo de equipo](docs/equipo.md)
- [Decisiones por hito](docs/decisiones.md)
- [Checkpoint 1](docs/checkpoint-01.md)

## 8. IA y autoría

- [x] Las consultas a IA están documentadas en `docs/decisiones.md`.
- [x] La interfaz (`templates/`) proviene de un proyecto previo del equipo y está declarada en `docs/decisiones.md`.
- [x] No hay secretos ni datos personales en el repositorio.

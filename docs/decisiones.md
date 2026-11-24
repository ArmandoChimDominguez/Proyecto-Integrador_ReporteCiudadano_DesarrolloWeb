# Decisiones del proyecto

**Equipo:** Pedro Pablo Pool Ché y Armando Chim Dominguez  
**Dominio:** Tablero → Tarea, adaptado a reportes ciudadanos

> Una página por hito: el registro de las decisiones que explican **por qué** el proyecto es como es.

---

## Origen del proyecto

La interfaz (`templates/SITIO` y `templates/ADMIN`) y la primera versión de `src/main.py` provienen de un proyecto previo del equipo en otra materia. En este curso se adaptan al contrato del Proyecto Integrador. Para el Hito 4 la interfaz se reemplazará por una sola página en JavaScript vanilla.

---

## Hito 1 · Contrato y mock

**Fecha:** 18/11/2026  
**Tag:** `v0.1-hito1`

- **Qué construí:** API en memoria con tableros (zonas) y tareas (reportes), relación 1:N, DTOs de Pydantic, sobre de error uniforme y 8 pruebas con pytest.
- **Decisión de diseño:** los listados se envuelven en un objeto (`{"tableros": [...]}`) y `DELETE` responde 204 sin cuerpo, como pide el contrato. El manejador de errores conserva los encabezados para que el 405 lleve `Allow`.
- **Alternativa descartada:** devolver arreglos sueltos en la raíz; no permiten agregar paginación después sin romper a los clientes.
- **Trade-off aceptado:** el almacenamiento en memoria se pierde al reiniciar; se acepta hasta el Hito 3 (SQLite).
- **Uso de IA:** se usó un asistente de IA (Claude) para revisar el contrato contra la guía, proponer las correcciones y redactar las 8 pruebas; se ejecutaron en Google Colab con resultado 8/8 y el equipo las revisó.
- **Qué falta para el Hito 2:** separar en capas (`routers`, `services`, `repositories`, `schemas`, `core`), registro y login con JWT, roles `user`/`admin` y 10 pruebas.

---

## Hito 2 · Capas y seguridad

**Fecha:** 18/11/2026  
**Tag:** `v0.2-hito2`

### Cómo separé las capas

| Capa | Archivos | Responsabilidad |
| :--- | :--- | :--- |
| Routers | `src/routers/auth.py`, `reportes.py`, `paginas.py` | Reciben HTTP, validan con los DTOs y llaman al servicio. No saben cómo se guardan los datos. |
| Servicios | `src/services/auth_service.py`, `reportes_service.py` | Reglas de negocio: registro, login, quién puede ver o borrar qué. Lanzan errores del dominio (`NoEncontrado`, `SinPermiso`, `Conflicto`), no `HTTPException`. |
| Repositorios | `src/repositories/memoria.py` | Guardan y buscan entidades. No importan FastAPI. Devuelven copias para que nadie modifique los datos por fuera. |
| Esquemas | `src/schemas/` | DTOs de entrada (`extra="forbid"`) y de salida. `UsuarioPublico` no tiene campo de contraseña. |
| Core | `src/core/config.py`, `security.py`, `dependencies.py` | Configuración desde el entorno, bcrypt + JWT y las dependencias de FastAPI. |

`main.py` solo arma la aplicación y traduce los errores del dominio a 401/403/404/409 con el sobre de error del proyecto.

### Dónde vive la seguridad

- **Contraseñas:** `core/security.py` guarda solo el hash bcrypt (costo 12). El DTO rechaza contraseñas de más de 72 bytes, que es el límite de bcrypt.
- **Login:** si el usuario no existe se compara contra un hash señuelo, para que la respuesta tarde lo mismo y no revele qué usuarios existen.
- **Token:** JWT HS256 con `sub` (id del usuario), `rol`, `iat` y `exp`. Se decodifica con el algoritmo fijo y exigiendo `exp`, `sub` y `rol`; cualquier token alterado o vencido es 401, nunca 500.
- **Autenticación (401):** dependencia `usuario_actual` con `HTTPBearer(auto_error=False)`, para que la falta de token sea 401 y no 403. El rol se toma del repositorio, no solo del token, así que un cambio de rol se aplica de inmediato.
- **Autorización (403):** en `ReportesService`: un `user` solo usa sus tableros y las tareas de esos tableros; un `admin` puede todo. Además está disponible `requiere_rol(...)` para rutas exclusivas de un rol.
- **Registro:** el rol de un usuario nuevo siempre es `user`; no se puede pedir `admin`.
- **Admin inicial:** solo se crea si se define `ADMIN_PASSWORD` en el entorno; no hay contraseñas en el código.

### Qué dependencia inyecté y por qué

- `get_repo_usuarios`, `get_repo_tableros` y `get_repo_tareas` (con `lru_cache`, una instancia por proceso) → `get_auth_service` y `get_reportes_service` → los endpoints los reciben con `Depends`.
- **Por qué:** las pruebas (`tests/conftest.py`) reemplazan los repositorios con `app.dependency_overrides` y cada prueba arranca con datos limpios **sin tocar ningún endpoint**. En el Hito 3 el repositorio en memoria se cambiará por uno con SQLAlchemy con los mismos métodos.

### Decisión, alternativa y trade-off

- **Decisión:** la regla de propiedad ("solo el dueño o un admin") vive en el servicio, no en el router, para que cualquier ruta nueva la respete.
- **Alternativa descartada:** poner el rol solo en el token y confiar en él. Era más simple, pero un usuario al que le quitan el rol seguiría con permisos hasta que su token expire.
- **Trade-off aceptado:** los usuarios siguen en memoria; al reiniciar hay que registrarse otra vez. Se resuelve en el Hito 3.
- **Cambio de contrato respecto al Hito 1:** todas las rutas `/api/tableros` y `/api/tareas` ahora exigen token, y el dueño de un tablero es el usuario autenticado (antes era `usuario_id = 1` fijo).

### Pruebas

18 en verde: las 8 del contrato del Hito 1 (ahora con token) y las 10 del Hito 2 en `tests/test_seguridad.py` (registro, duplicado 409, login correcto e incorrecto, perfil con token, sin token 401, token alterado 401, el dueño borra 204, otro usuario 403 y el admin lista todos). Se ejecutaron en Google Colab: `18 passed`.

### Uso de IA

Se usó un asistente de IA (Claude) para proponer la separación en capas, el manejo de errores del dominio y las pruebas, a partir de lo practicado en los laboratorios 15–20. El equipo revisó el código, y las pruebas se ejecutaron y pasaron antes de crear el tag.

### Qué falta para el Hito 3

Persistencia con SQLite + SQLAlchemy (repositorio con los mismos métodos), migraciones con Alembic y la revisión OWASP.

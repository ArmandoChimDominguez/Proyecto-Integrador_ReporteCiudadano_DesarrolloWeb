# Propuesta del Proyecto Integrador

**Curso:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Equipo:** Pedro Pablo Pool Ché y `BrokeniGS` (L23531079)  
**Dominio elegido:** Tablero → Tarea, adaptado a reportes ciudadanos  
**Repositorio:** https://github.com/XxZoroxX10/Proyecto-Integrador_ReporteCiudadano_DesarrolloWeb  
**Fecha:** 18/11/2026

> La adaptación del dominio está pendiente de confirmación escrita del docente (ver checkpoint 1).

---

## 1. Problema y usuario

En las colonias, los reportes de baches, alumbrado y basura se pierden en llamadas o redes sociales y nadie sabe en qué estado van. La API permite registrar cada reporte en un tablero por zona y darle seguimiento (pendiente → en progreso → resuelta). La usan los vecinos para reportar y un administrador para revisar.

## 2. Entidades

### Entidad principal: Tablero (zona)

| Campo | Tipo | Obligatorio | Regla |
| :--- | :--- | :---: | :--- |
| id | entero | sí | generado por el servidor |
| nombre | texto | sí | 3–60 caracteres |
| descripcion | texto | no | máximo 250 caracteres |
| usuario_id | entero | sí | dueño del registro |

### Entidad secundaria: Tarea (reporte ciudadano)

| Campo | Tipo | Obligatorio | Regla |
| :--- | :--- | :---: | :--- |
| id | entero | sí | generado por el servidor |
| tablero_id | entero | sí | llave foránea; el tablero debe existir |
| titulo | texto | sí | 5–100 caracteres |
| descripcion | texto | sí | 10–500 caracteres |
| categoria | texto | sí | `baches`, `alumbrado` o `basura` |
| ubicacion | texto | sí | 5–150 caracteres |
| estado | texto | no | `pendiente` (por defecto), `en_progreso` o `resuelta` |

### Usuario

| Campo | Tipo | Regla |
| :--- | :--- | :--- |
| id | entero | generado por el servidor |
| usuario | texto | único, 3–30 caracteres |
| password_hash | texto | nunca se devuelve |
| rol | texto | `user` o `admin` |

**Relación:** Tablero 1 → N Tarea.

## 3. Endpoints

| # | Método | Ruta | Qué hace | Auth | Hito |
| :---: | :--- | :--- | :--- | :---: | :---: |
| 1 | POST | `/api/registro` | Crea usuario | No | 2 |
| 2 | POST | `/api/token` | Login y JWT | No | 2 |
| 3 | GET | `/api/tableros` | Lista los míos | Sí | 1* |
| 4 | POST | `/api/tableros` | Crea tablero | Sí | 1* |
| 5 | GET | `/api/tableros/{id}/tareas` | Lista reportes | Sí | 1* |
| 6 | POST | `/api/tableros/{id}/tareas` | Crea reporte | Sí | 1* |
| 7 | GET | `/api/tareas/{id}` | Consulta reporte | Sí | 1* |
| 8 | DELETE | `/api/tareas/{id}` | Elimina reporte | Sí | 1* |
| 9 | GET | `/health` | Estado | No | 1* |
| 10 | GET | `/api/tableros/{id}/tareas?estado=pendiente` | Filtro por estado | Sí | 3 |

## 4. Reglas de negocio

1. `categoria` solo puede ser `baches`, `alumbrado` o `basura`.
2. `estado` solo puede ser `pendiente`, `en_progreso` o `resuelta`; inicia en `pendiente`.
3. No se puede crear un reporte en un tablero que no existe (404).
4. Solo el dueño o un admin puede eliminar un reporte (Hito 2).
5. Filtro por estado en el listado de reportes (Hito 3).

## 5. Casos de prueba del Hito 1

| # | Caso | Entrada | Resultado esperado |
| :---: | :--- | :--- | :--- |
| 1 | Crear tablero válido | `{"nombre":"Colonia Centro"}` | 201 |
| 2 | Crear tablero inválido | `{"nombre":"AB"}` | 422 |
| 3 | Listar tableros | — | 200 |
| 4 | Crear reporte válido | reporte completo | 201 |
| 5 | Reporte en tablero inexistente | tablero 999 | 404 |
| 6 | Listar reportes del tablero | tablero 1 | 200 |
| 7 | Eliminar reporte y consultarlo | reporte 1 | 204 y luego 404 |
| 8 | Método no permitido | `PATCH /api/tareas/1` | 405 |

## 6. Riesgos y mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
| :--- | :---: | :---: | :--- |
| El docente no aprueba la adaptación del dominio | media | alto | Preguntar en el checkpoint 1; si no se aprueba, ajustar los campos a Tablero → Tarea del catálogo |
| La interfaz previa excede el alcance (varias páginas) | alta | medio | Para el Hito 4 hacer una sola página con JS vanilla que consuma la API |
| Poco tiempo entre hitos | media | medio | Repartir backend y pruebas, y avanzar con las pruebas desde el inicio |

## 7. Plan por hito

| Hito | Qué tendremos listo | Responsable principal |
| :--- | :--- | :--- |
| 1 | Mock API, OpenAPI, 8 pruebas | Ambos |
| 2 | Capas, auth JWT, RBAC, 10 pruebas | Por definir |
| 3 | SQLite, Alembic, OWASP, 12 pruebas | Por definir |
| 4 | SPA, Dockerfile, demo | Por definir |

## 8. Roles y compromiso

| Integrante | Rol principal |
| :--- | :--- |
| Pedro Pablo Pool Ché | Backend, pruebas y documentación |
| `BrokeniGS` | Frontend e integración |

- [ ] Ambos leyeron la guía oficial.
- [ ] Ambos aceptan el alcance y las reglas.
- [ ] Ambos se comprometen a tener al menos un commit por hito.

## 9. Declaración de alcance

- [x] Usa **2 entidades de negocio + usuario**.
- [x] Tiene **8–10 endpoints**.
- [x] No incluye pagos, chat, tiempo real, IA, apps móviles ni APIs externas.
- [x] Usa el stack permitido.
- [x] No copia el dominio ni el código de los laboratorios.

**Firmas:** Pedro Pablo Pool Ché · `BrokeniGS`

# Checkpoint del Proyecto Integrador

**Equipo:** Pedro Pablo Pool Ché y Armando Chim Dominguez (`BrokeniGS`)  
**Dominio:** Tablero → Tarea, adaptado a reportes ciudadanos  
**Checkpoint:** 01  
**Hito en curso:** 1 (cierre) → H2  
**Fecha:** 18/11/2026  
**Repositorio:** https://github.com/XxZoroxX10/Proyecto-Integrador_ReporteCiudadano_DesarrolloWeb

---

## 1. Hecho (con evidencia)

- [x] API en memoria con tableros (zonas) y tareas (reportes), relación 1:N — evidencia: `src/main.py`, commit `362b1ca`
- [x] Contrato del Hito 1: 201 al crear, 422 con sobre de error, 404 en padre inexistente, `DELETE` 204, 405 con `Allow`, listados envueltos en objeto — evidencia: commit `362b1ca`
- [x] 8 pruebas con pytest que revisan código y cuerpo — evidencia: `tests/test_api.py`, commit `52ab229`
- [x] `/health`, `/docs` y `/openapi.json` con los modelos `TableroResponse`, `TareaResponse`, `ListaTableros` y `ListaTareas`

**Tag o commit actual:** `52ab229` (tag `v0.1-hito1` pendiente)  
**Pruebas en verde:** `8/8`  
**OpenAPI:** `http://127.0.0.1:8000/docs` al ejecutar `uvicorn src.main:app --reload`

## 2. Siguiente

1. [ ] Crear el tag `v0.1-hito1` sobre el commit que cierra el Hito 1.
2. [ ] Separar en capas: `routers/`, `services/`, `repositories/`, `schemas/`, `core/`.
3. [ ] Registro con hash bcrypt y login con JWT (`sub`, `rol`, `exp`).
4. [ ] Roles `user`/`admin`: cada usuario ve solo sus tableros; borrar ajeno → 403; sin token → 401.
5. [ ] Llegar a 10 pruebas.

**Fecha estimada de cierre del Hito 2:** sesión 20.

## 3. Bloqueo

- Necesitamos confirmación del docente sobre la adaptación del dominio (ver preguntas).

## 4. Demo de 3 minutos

1. Abrir `/docs`.
2. Crear un tablero «Colonia Centro».
3. Crear un reporte de bache en ese tablero.
4. Listar los reportes del tablero.
5. Eliminar el reporte (204) y consultarlo (404).
6. Enviar un tablero con nombre de 2 letras y mostrar el 422 con el sobre de error.
7. Cerrar con `pytest -q` → 8 passed.

## 5. Evidencia de pruebas

```text
tests/test_api.py::test_crear_tablero_valido PASSED                      [ 12%]
tests/test_api.py::test_crear_tablero_invalido PASSED                    [ 25%]
tests/test_api.py::test_listar_tableros PASSED                           [ 37%]
tests/test_api.py::test_crear_tarea_valida PASSED                        [ 50%]
tests/test_api.py::test_crear_tarea_en_tablero_inexistente PASSED        [ 62%]
tests/test_api.py::test_listar_tareas_del_tablero PASSED                 [ 75%]
tests/test_api.py::test_eliminar_tarea_y_consultarla PASSED              [ 87%]
tests/test_api.py::test_verbo_no_permitido PASSED                        [100%]

============================== 8 passed in 0.89s ===============================
```

## 6. Preguntas para el docente

- Usamos las rutas de Tablero → Tarea, pero cada tarea es un **reporte ciudadano** (`categoria`: baches, alumbrado o basura; `ubicacion`; estado `pendiente`/`en_progreso`/`resuelta`) en lugar de `prioridad` y `fecha_limite`. ¿Se aprueba esta adaptación o debemos ajustarnos a los campos del catálogo?
- La interfaz actual (varias páginas) viene de un proyecto previo del equipo. ¿Es válido reemplazarla en el Hito 4 por una sola página en JavaScript vanilla, como pide la guía?

## 7. Compromiso del equipo

- [ ] Ambos revisaron este checkpoint.
- [ ] El siguiente paso tiene responsable y fecha.
- [x] El repositorio está actualizado y el commit es accesible.

**Firmas:** Pedro Pablo Pool Ché · Armando Chim Dominguez

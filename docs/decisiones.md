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

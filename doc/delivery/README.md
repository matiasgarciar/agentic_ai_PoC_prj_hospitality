# AI Hospitality Workshop – Delivery

## 1. Objetivo
Este documento describe la solución final entregada para el **AI Hospitality Workshop**, cuyo objetivo es construir un sistema **Agentic AI** capaz de responder consultas hoteleras utilizando:

- Respuestas simples (Exercise 0)
- Recuperación de información no estructurada mediante **RAG + Vector DB** (Exercise 1)
- Analítica sobre datos estructurados vía **SQL** (Exercise 2)

La solución está diseñada para ser **reproducible end-to-end** mediante Docker.

---

## 2. Arquitectura General

El sistema se compone de los siguientes elementos:

- **Frontend (UI Web)**: Interfaz de chat para lanzar queries
- **AI Agents API**: Servicio FastAPI que orquesta los agentes
- **Vector Database (ChromaDB)**: Base de datos vectorial para RAG
- **PostgreSQL**: Base de datos relacional para bookings

La arquitectura completa y el árbol de agentes están documentados mediante **Excalidraw** y se incluyen en este directorio.

---

## 3. Agentes y responsabilidades

### Orchestrator Agent
Responsable de:
- Recibir la query del usuario
- Determinar el modo de ejecución (simple / rag / sql)
- Delegar la consulta al agente especializado

### Agentes especializados

- **Hotel Simple Agent (Exercise 0)**  
  Respuestas simples y estáticas.

- **Hotel RAG Agent (Exercise 1)**  
  Recupera información hotelera desde documentos no estructurados indexados en ChromaDB.

- **Booking SQL Agent (Exercise 2)**  
  Ejecuta queries analíticas sobre PostgreSQL (revenue, RevPAR, occupancy, etc.).

---

## 4. Fuentes de datos

- **Datos no estructurados**: Documentación de hoteles y habitaciones (`bookings-db/output_files/hotels/*.md`)
- **Datos estructurados**: Base de datos PostgreSQL con reservas (`bookings-db`)

---

## 5. Cómo ejecutar la solución

Desde la raíz del proyecto:

```bash
cd prj-docker-compose
./start-app.sh --logs
```

Esto levantará automáticamente:
- AI Agents API
- PostgreSQL
- Vector DB (Chroma)

La UI estará disponible en:

```
http://localhost:8001
```

Para detener todos los servicios:

```bash
./stop-app.sh
```

---

## 6. Validación

La validación se realiza:

1. Ejecutando el stack completo con `start-app.sh --logs`
2. Ejecutando los tests automáticos de Exercise 1
3. Probando queries desde la UI

Los detalles completos de las pruebas se describen en `tests.md`.

---

## 7. Consideraciones técnicas

- La base de datos vectorial se ejecuta como **servicio Docker independiente**, con volumen persistente.
- El sistema maneja correctamente queries sin información disponible (edge cases).
- Las variables sensibles (API keys) **no se incluyen en el repositorio** y se gestionan mediante `.env`.

---

## 8. Evidencias

- Capturas de la UI
- Diagramas de arquitectura
- Resultados de tests

Todo el material se incluye en este directorio `doc/delivery/`.


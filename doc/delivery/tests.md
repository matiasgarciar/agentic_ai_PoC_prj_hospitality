# Tests – AI Hospitality Workshop

## Objetivo
Este documento describe el **set de pruebas funcionales** utilizado para validar la correcta implementación del Workshop, especialmente el **Exercise 1 (RAG Agent)**.

---

## 1. Entorno de prueba

- Ejecución mediante Docker Compose
- Servicios activos:
  - ai_agents_hospitality-api
  - vector-db (ChromaDB)
  - bookings-db (PostgreSQL)

Comando de arranque:

```bash
./start-app.sh --logs
```

---

## 2. Pruebas automáticas (CLI)

Archivo ejecutado:

```
ai_agents_hospitality-api/test_exercise_1.py
```

Comando:

```bash
docker exec -it ai_agents_hospitality-api sh -lc "python test_exercise_1.py"
```

---

## 3. Queries esperadas (Exercise 1)

### Q1 – Dirección completa de un hotel
**Query:**
```
What is the full address of Obsidian Tower?
```
**Resultado esperado:**
- Dirección completa
- Ciudad
- País

---

### Q2 – Cargos de Half Board en París
**Query:**
```
What are the meal charges for Half Board in hotels in Paris?
```
**Resultado esperado:**
- Peso / multiplicador de Half Board
- Contexto de precios

---

### Q3 – Hoteles en Francia
**Query:**
```
List all hotels in France with their cities
```
**Resultado esperado:**
- Lista de hoteles
- Ciudad asociada

---

### Q4 – Descuento por cama extra (edge case)
**Query:**
```
What is the discount for extra bed in Grand Victoria?
```
**Resultado esperado:**
- Mensaje indicando que la información no está disponible

> Esta prueba valida el manejo correcto de datos inexistentes.

---

### Q5 – Comparativa peak vs off season
**Query:**
```
Compare room prices between peak and off season for hotels in Nice
```
**Resultado esperado:**
- Tabla comparativa
- Diferencias de precio
- Resumen textual

---

## 4. Pruebas manuales (UI)

Las mismas queries se ejecutaron desde la interfaz web:

```
http://localhost:8001
```

Resultados observados:
- Respuestas coherentes
- Uso correcto de RAG
- Manejo adecuado de edge cases

---

## 5. Resultado final

✅ Todas las queries críticas funcionan correctamente  
⚠️ La query de descuento por cama extra no existe en los datos (comportamiento esperado)

El sistema se considera **válido y estable para la entrega**.

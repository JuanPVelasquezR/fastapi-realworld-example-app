---
name: "Reporte de Defecto (Bug Report)"
about: "Plantilla formal de reporte de defectos basada en ISTQB y el marco normativo de pruebas de software"
title: "[BUG-XX]: <Resumen conciso del defecto (máx 80 caracteres)>"
labels: ["bug", "triage-needed"]
assignees: []
---

## 📋 Control y Metadatos del Defecto

| Parámetro | Detalle |
|---|---|
| **ID del Defecto** | `BUG-XX` (Vinculado a este Issue de GitHub) |
| **Módulo Afectado** | `Auth` / `Articles` / `Comments` / `Profiles` / `Favorites` / `Tags` |
| **Caso(s) de Prueba Asociado(s)** | `CP-[MOD]-[TIPO]-[NUM]` (Trazabilidad bidireccional) |
| **Severidad Técnica** | `Crítica` / `Alta` / `Media` / `Baja` |
| **Prioridad de Negocio** | `Alta` / `Media` / `Baja` |
| **Estado del Ciclo de Vida** | `[x] Abierto (Open)` / `[ ] En Progreso` / `[ ] Resuelto` / `[ ] Cerrado` |
| **Entorno de Pruebas** | `localhost:8000` • Rama `buggy-version` • Python 3.14 • PostgreSQL (Docker) |
| **Reportado por** | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas |
| **Fecha de Reporte** | DD/MM/AAAA |
| **Asignado a** | Equipo de Desarrollo / Niurka Liseth Mejía Vargas (Bug Manager) |

---

## 🧬 Cadena Causal ISTQB (§2.1 Contexto de Clase)

> De acuerdo con la taxonomía formal de calidad de software:
> **Error Humano** $\rightarrow$ genera un **Defecto estático en el código** $\rightarrow$ se manifiesta como un **Fallo dinámico observable**.

* **Error Humano:** *(Acción humana incorrecta durante el diseño, especificación o codificación).*
* **Defecto en Código (Bug / Causa Raíz):** *(Archivo, función, línea de código exacta o instrucción defectuosa en el repositorio).*
* **Fallo Dinámico Observable:** *(Manifestación externa en tiempo de ejecución: código HTTP erróneo, excepción 500, alteración indebida de datos).*

---

## 💼 Justificación de Impacto en el Modelo de Negocio (§2.2 y §3.1)

* **Impacto en el Negocio (Plataforma tipo Medium):** *(Explicar cómo afecta a los autores, lectores, integridad editorial, confidencialidad o disponibilidad del sistema).*
* **Justificación de Severidad (Dimensión Técnica):** *(Impacto en la arquitectura, base de datos o estabilidad del backend).*
* **Justificación de Prioridad (Dimensión de Negocio):** *(Urgencia requerida para la resolución del defecto según el riesgo operacional).*

---

## ⚙️ Precondiciones y Datos de Prueba

1. El entorno backend FastAPI debe estar levantado y conectado a PostgreSQL.
2. Estado previo requerido en la base de datos (usuarios, artículos o tokens específicos).
3. Headers requeridos (`Content-Type: application/json`, `Authorization: Bearer <token>`).

---

## 🔁 Pasos para Reproducir (Step-by-Step)

1. Enviar una petición HTTP con los siguientes parámetros:
   * **Método:** `GET` / `POST` / `PUT` / `DELETE`
   * **Endpoint:** `http://localhost:8000/api/...`
   * **Headers:**
     ```http
     Authorization: Bearer <token>
     Content-Type: application/json
     ```
   * **Payload JSON:**
     ```json
     {
       "objeto": {
         "campo": "valor"
       }
     }
     ```
2. Ejecutar la petición en Swagger UI, Postman o mediante script de integración.
3. Observar la respuesta HTTP del servidor.

---

## 🎯 Comportamiento Esperado vs. Obtenido

* **Resultado Esperado (Normativo - RealWorld Spec):**
  * **Código de Estado HTTP:** `HTTP 20X` / `HTTP 40X`
  * **Cuerpo de Respuesta:** Estructura JSON conforme a la especificación oficial.
  * **Efecto Colateral:** Comportamiento esperado en base de datos.
* **Resultado Obtenido (Real / Falla Detectada):**
  * **Código de Estado HTTP:** `HTTP ...`
  * **Cuerpo de Respuesta:** Estructura errónea o mensaje de excepción.
  * **Efecto Colateral:** Discrepancia real observada.

---

## 📸 Evidencias Técnicas

### 🧪 Evidencia Automatizada (pytest)
```text
[Pegar aquí el traceback de fallo de pytest con aserción y módulo]
```

### 🖼️ Evidencia Manual (Swagger UI / Postman)
* **Captura:** `docs_qa/evidencias/[NOMBRE_ARCHIVO].png`
* *(Arrastrar o vincular la imagen aquí en GitHub Issues)*

---

## 🛡️ Criterios de Cierre y Verificación (Definition of Done)

- [ ] Defecto corregido en rama de desarrollo.
- [ ] Prueba de regresión automatizada (`pytest tests/test_...py`) ejecutada y pasando en verde (`PASSED`).
- [ ] Verificación manual en Swagger UI / Postman confirmada.
- [ ] Issue cerrado con commit de resolución referenciado (`Fixes #[Issue]`).


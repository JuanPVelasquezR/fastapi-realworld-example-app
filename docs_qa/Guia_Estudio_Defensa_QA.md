# MANUAL MAESTRO DE ESTUDIO Y DEFENSA TÉCNICA
## Taller de Pruebas de Software — FastAPI RealWorld Example App (Conduit API)

---

> ### 📌 FICHA TÉCNICA Y METADATOS DEL PROYECTO
> * **Sistema Bajo Prueba (SUT):** Conduit REST API (FastAPI + PostgreSQL + Docker).
> * **Especificación Funcional:** *RealWorld Backend API Spec* (Contrato estándar de facto de la industria).
> * **Equipo de Calidad (QA Engineers):** 
>   * **Juan Pablo Velásquez Ramírez** — QA Lead, Automatizador de Pruebas & Analista Técnico.
>   * **Niurka Liseth Mejía Vargas** — QA Analyst, Bug Manager & Gestora de Documentación / Métricas.
> * **Supervisora y Docente:** Yury Montoya Pérez.
> * **Rama Base Limpia:** `main` (100% de pruebas aprobadas, sin defectos).
> * **Rama de Evaluación / Detección:** `buggy-version` (9 defectos reales inyectados).
> * **Resultado del Ciclo STLC:** **41 Casos de Prueba Ejecutados (100%)**, **9 Defectos Detectados (100% DRE)**, **Dictamen Formal: NO-GO (Bloqueo de Pase a Producción)**.

---

## ÍNDICE GENERAL DEL MANUAL
1. **Módulo 1:** Radiografía del Sistema Bajo Prueba (SUT) y Arquitectura FastAPI.
2. **Módulo 2:** El Modelo de Negocio (Plataforma Editorial Medium) y su Impacto en Calidad.
3. **Módulo 3:** Compendio Teórico Formal de Pruebas de Software (Normativa ISTQB).
4. **Módulo 4:** Estrategia STLC y Catálogo de 41 Casos de Prueba (26 Automatizados + 15 Manuales).
5. **Módulo 5:** Radiografía Profunda de los 9 Defectos Detectados (Bugs 01 al 09).
6. **Módulo 6:** Gestión de Defectos en GitHub Issues y Trazabilidad.
7. **Módulo 7:** Métricas Cuantitativas de Calidad y Tablero de Control (Dashboard).
8. **Módulo 8:** Análisis de Calidad y Fundamentación del Dictamen NO-GO.
9. **Módulo 9:** Glosario Técnico Maestro (25+ Conceptos Clave que Debes Dominar).
10. **Módulo 10:** Banco de 10 Preguntas Trampa / Exigentes de la Docente y Cómo Responderlas.
11. **Módulo 11 (Cierre):** Estructura Sugerida de Exposición Oral y Guion de Defensa.

---

# MÓDULO 1: RADIOGRAFÍA DEL SISTEMA BAJO PRUEBA (SUT) Y ARQUITECTURA

### 1.1 ¿Qué es Conduit y por qué se eligió?
Conduit es la implementación oficial de referencia de la especificación **RealWorld**. En la ingeniería de software, mientras aplicaciones de juguete como "TodoMVC" solo muestran operaciones elementales, la especificación RealWorld emula una plataforma de producción completa: una red social de publicaciones y artículos tipo **Medium**, **Dev.to** o **Substack**.

No posee interfaz gráfica propia (es un backend puro de servicios RESTful). Esto hace que las pruebas sean directas sobre la lógica de negocio, los contratos HTTP, la persistencia en base de datos y la seguridad a nivel de API.

### 1.2 El Stack Tecnológico y su Justificación
* **FastAPI (Python):** Framework web asincrónico moderno de alto rendimiento basado en **Starlette** (manejo ASGI y rutas) y **Pydantic** (validación de datos y serialización mediante type hints).
* **Uvicorn:** Servidor web ASGI (Asynchronous Server Gateway Interface) ultrarrápido que maneja concurrencia mediante el bucle de eventos (`asyncio`).
* **PostgreSQL:** Sistema gestor de base de datos relacional robusto. Garantiza transacciones ACID e integridad referencial estricta (claves foráneas en cascada entre usuarios, artículos, comentarios, tags y favoritos).
* **SQLAlchemy ORM:** Mapeador objeto-relacional que traduce clases de Python en tablas y consultas relacionales, abstrayendo la manipulación directa de SQL.
* **Alembic:** Herramienta de migraciones de esquemas de base de datos para versionar la estructura de PostgreSQL.
* **Pytest + Pytest-Asyncio + HTTPX:** Ecosistema moderno de pruebas en Python. Permite ejecutar peticiones asincrónicas contra el kernel de la aplicación mediante `AsyncClient`, sin requerir levantar un puerto de red real durante los tests.
* **Docker & Docker Compose:** Contenedorización del entorno de base de datos y de la aplicación, garantizando que el ambiente de pruebas sea 100% reproducible y desacoplado del sistema operativo anfitrión.

### 1.3 Anatomía en Capas del Backend
Para defender el trabajo ante la docente, debes explicar la separación de responsabilidades del código:

```text
[ Petición HTTP del Cliente (Swagger / Postman / pytest) ]
                           │
                           ▼
 ┌─────────────────────────────────────────────────────────┐
 │ 1. Capa de Enrutamiento (app/api/routes/)               │
 │    Define endpoints, verbos HTTP (GET, POST, PUT,       │
 │    DELETE) y códigos de estado (status codes).          │
 └─────────────────────────┬───────────────────────────────┘
                           │ Valida Payload
                           ▼
 ┌─────────────────────────────────────────────────────────┐
 │ 2. Capa de Esquemas DTO (app/schemas/)                  │
 │    Modelos Pydantic (NewArticle, UpdateArticle, User).  │
 │    Rechaza datos inválidos con HTTP 422.                │
 └─────────────────────────┬───────────────────────────────┘
                           │ Inyecta Usuario
                           ▼
 ┌─────────────────────────────────────────────────────────┐
 │ 3. Capa de Dependencias y Seguridad (app/api/deps.py)   │
 │    Extrae el token JWT del header Authorization,        │
 │    desencripta y valida la identidad del usuario actual. │
 └─────────────────────────┬───────────────────────────────┘
                           │ Llama Operaciones
                           ▼
 ┌─────────────────────────────────────────────────────────┐
 │ 4. Capa de Repositorios / CRUD (app/crud/)              │
 │    Lógica de acceso a datos (crud_article.py,           │
 │    crud_user.py). Construye queries de SQLAlchemy.      │
 └─────────────────────────┬───────────────────────────────┘
                           │ Persiste
                           ▼
 ┌─────────────────────────────────────────────────────────┐
 │ 5. Capa de Modelos y Base de Datos (app/models/)        │
 │    Tablas relacionales en PostgreSQL (users, articles,  │
 │    comments, tags, followers, favorites).               │
 └─────────────────────────┘
```

### 1.4 La Estrategia de Dos Ramas en Git
Una de las decisiones metodológicas más elegantes del proyecto fue el manejo de versiones en Git:

* **Rama `main` (Limpia / Baseline):** Contiene el código fuente original sin alteraciones. Al ejecutar los 26 tests automatizados de pytest, los 26 aprueban (**100% Pass** en 28.92 segundos). Sirve como prueba matemática de que la suite de pruebas no tiene "falsos positivos".
* **Rama `buggy-version` (Evaluación / Inyección de Fallos):** Se crearon 9 alteraciones deliberadas en puntos críticos del backend. Al ejecutar la misma suite de pruebas, 11 tests automatizados y 6 pruebas manuales fallaron con precisión milimétrica, confirmando que la red de seguridad de QA detecta anomalías reales.

---

# MÓDULO 2: EL MODELO DE NEGOCIO Y SU IMPACTO EN CALIDAD

### 2.1 ¿Por qué el Modelo de Negocio Determina las Pruebas?
La docente insistió en clase: *"El testing no se hace en el vacío; el contexto del negocio define qué es prioritario y qué es secundario"*. 

Conduit no es una calculadora ni un sistema de comercio electrónico de pagos bancarios; es una **plataforma editorial y red de contenido abierto**. En este tipo de negocio, el valor fundamental radica en la **confianza del autor**, la **integridad de las publicaciones** y la **fidelización del lector**.

### 2.2 Jerarquía de Riesgo de Negocio en Conduit
* **Nivel 1: Autenticación y Autoría (Vital / Crítico):**  
  Si un usuario puede usurpar la autoría, editar las publicaciones de otro autor o borrar artículos ajenos, la plataforma pierde inmediatamente a sus creadores de contenido. La propiedad intelectual es el activo intangible más valioso. Por ello, las fallas de autorización (BOLA) son catalogadas con **Severidad Crítica** y **Prioridad Inmediata**.
* **Nivel 2: Integridad Editorial y Navegabilidad (Alto):**  
  Un artículo no puede publicarse sin título ni contenido. Los artículos vacíos corrompen los algoritmos de recomendación, rompen los feeds de noticias y arruinan la indexación de búsqueda (SEO).
* **Nivel 3: Engagement Social (Medio):**  
  Los botones de "Favorito" y "Seguir autor" retienen a los lectores. Si fallan (como el error 500 en favoritos o el estado estático en seguir), el usuario siente frustración visual, aunque los artículos continúan siendo legibles.
* **Nivel 4: Taxonomía y Metadatos (Bajo):**  
  Las etiquetas (tags) ayudan a categorizar. Si un filtro devuelve un artículo de más, es una inconsistencia molesta pero no detiene la lectura ni corrompe información patrimonial.

---

# MÓDULO 3: COMPENDIO TEÓRICO FORMAL DE PRUEBAS DE SOFTWARE (ISTQB)

### 3.1 QA (Quality Assurance) vs. QC (Quality Control)
| Criterio | Quality Assurance (QA) | Quality Control (QC) |
|---|---|---|
| **Enfoque** | Orientado al **proceso** de ingeniería. | Orientado al **producto** final de software. |
| **Naturaleza** | **Proactiva:** Previene la aparición de defectos mediante estándares, guías y diseño temprano. | **Reactiva:** Detecta defectos preexistentes mediante la ejecución de pruebas. |
| **Responsabilidad** | Transversal a todo el equipo (Devs, QA, Líderes). | Asignada específicamente al equipo de pruebas. |
| **Momento** | Continuo a lo largo de todo el ciclo de vida (SDLC). | Posterior a la construcción o disponibilidad del artefacto. |

### 3.2 Verificación vs. Validación (El Modelo de Boehm)
* **Verificación:** *"¿Estamos construyendo el producto correctamente?"*  
  Comprueba que el software cumple de manera estricta y sintáctica con las especificaciones técnicas y requisitos de entrada (RFCs, contratos REST, esquemas Pydantic).
* **Validación:** *"¿Estamos construyendo el producto correcto?"*  
  Comprueba que el sistema satisface las necesidades reales, expectativas operacionales y reglas de negocio del usuario final y los *stakeholders*.

### 3.3 La Cadena Causal de las Anomalías (§2.1 de los apuntes)
ISTQB establece una distinción científica obligatoria entre tres conceptos que los desarrolladores suelen confundir:

> **CADENA CAUSAL ISTQB:**  
> **Error Humano** &nbsp;→&nbsp; **Defecto en Código (Bug)** &nbsp;→&nbsp; **Fallo Dinámico Observable**

1. **Error (Human Error):** Acción u omisión humana equivocada cometida por el ingeniero durante el análisis, arquitectura o codificación.  
   *Ejemplo en el proyecto:* El desarrollador olvidó escribir la condición `if article.author_id != current_user.id: raise HTTPException(400)`.
2. **Defecto (Bug / Causa Raíz):** Imperfección o anomalía estática presente en el producto de trabajo (el código fuente, script o esquema).  
   *Ejemplo en el proyecto:* La línea ausente en `app/api/routes/articles/articles.py` línea 85.
3. **Fallo (Failure):** Evento dinámico observable en tiempo de ejecución en el cual el sistema deja de realizar la función requerida o la realiza de forma incorrecta.  
   *Ejemplo en el proyecto:* La API responde con `HTTP 200 OK` y borra de la base de datos el artículo de Laura cuando la petición la envió Carlos.

### 3.4 Dimensiones de Evaluación: Severidad Técnica vs. Prioridad de Negocio
* **Severidad (Métrica Técnica):** Mide el grado de impacto técnico, daño estructural o degradación que el defecto causa sobre el software, la base de datos o el hardware. Se clasifica en: `Crítica`, `Alta`, `Media`, `Baja`.
* **Prioridad (Métrica de Negocio / Gestión):** Determina la urgencia o prelación cronológica con la que el defecto debe ser resuelto en el plan de trabajo del equipo de desarrollo. Se clasifica en: `Alta`, `Media`, `Baja`.

> **Pregunta de examen:** *¿Puede haber un bug de Severidad Baja pero Prioridad Alta?*  
> **Respuesta:** Sí. Por ejemplo, el logotipo de la empresa aparece mal escrito o invertido en la portada principal. Técnicamente no rompe nada (Severidad Baja), pero comercialmente daña la marca de inmediato (Prioridad Alta).  
> En nuestro proyecto, el **BUG-04** tiene tanto **Severidad Crítica** (borrado irreversible de base de datos) como **Prioridad Alta** (bloqueante absoluto).

### 3.5 Los 7 Principios Fundamentales del Testing (ISTQB)
1. **Las pruebas muestran la presencia de defectos, no su ausencia:** Probar un sistema permite encontrar fallos, pero es teóricamente imposible demostrar matemáticamente que no queda ningún error oculto.
2. **Las pruebas exhaustivas no son posibles:** Probar todas las combinaciones posibles de datos, entradas y precondiciones es inviable. Por eso se usan técnicas como Partición de Equivalencia y BVA para seleccionar muestras representativas.
3. **Pruebas tempranas:** Iniciar las pruebas lo antes posible (en fase de requisitos y diseño) ahorra costos exponenciales de retrabajo.
4. **Agrupamiento de defectos (*Defect clustering*):** La mayoría de los defectos se concentran en un pequeño número de módulos críticos. *(En Conduit, el 66.7% de los bugs se concentraron en el módulo Articles)*.
5. **La paradoja del pesticida:** Si los mismos casos de prueba se repiten una y otra vez, con el tiempo dejan de encontrar defectos nuevos. La suite debe evolucionar.
6. **Las pruebas dependen del contexto:** No se prueba igual una API de blog, que un software de aviónica o una pasarela de pagos médicos.
7. **La falacia de ausencia de errores:** Reparar el 100% de los defectos no garantiza el éxito del producto si el sistema construido no sirve a las necesidades reales del usuario.

### 3.6 Ciclo de Vida: SDLC vs. STLC
* **SDLC (Software Development Life Cycle - ISO/IEC 12207):** Ciclo completo de desarrollo del software (Planeación, Análisis, Diseño, Construcción, Pruebas y Despliegue).
* **STLC (Software Testing Life Cycle):** Subproceso disciplinado de aseguramiento de calidad con 5 fases secuenciales y 2 transversales:
  * **Fase 1: Test Analysis (Análisis):** ¿Qué probar? Identificación de condiciones de prueba y base normativa.
  * **Fase 2: Test Design (Diseño):** ¿Cómo probar? Especificación formal de los casos de prueba y datos.
  * **Fase 3: Test Implementation (Implementación):** ¿Está todo listo? Construcción de scripts pytest, ambiente Docker y datos de prueba.
  * **Fase 4: Test Execution (Ejecución):** Comparación del comportamiento real vs. esperado, captura de evidencias y reporte de defectos.
  * **Fase 5: Test Completion (Cierre):** Criterios de cierre, métricas, reporte de resumen (Test Summary Report) y archivo de artefactos (*testware*).
  * **Transversales:** **Test Planning** (Planificación estratégica) y **Test Monitoring & Control** (Seguimiento continuo).

---

# MÓDULO 4: ESTRATEGIA STLC Y CATÁLOGO DE 41 CASOS DE PRUEBA

### 4.1 Nomenclatura Estándar de Casos de Prueba
Cada caso de prueba posee un identificador estructurado y trazable:

> **Formato:** `CP - [MÓDULO] - [MODO] - [NÚMERO]`  
> *Ejemplo:* `CP-AUTH-A-001` (Automatizado), `CP-QUAL-M-004` (Manual)

* **Módulo:** `AUTH` (Autenticación), `ART` (Artículos), `COM` (Comentarios), `PRF` (Perfiles), `FAV` (Favoritos), `TAG` (Etiquetas), `EXP` (Exploratorias), `TOOL` (Herramientas), `QUAL` (Calidad/Seguridad), `EST` (Estados).
* **Modo:** `A` (Automatizado con `pytest`), `M` (Manual con `Swagger UI / Postman`).

### 4.2 Matriz de Distribución de los 41 Casos
El equipo superó la meta mínima de 40 casos, diseñando y ejecutando **41 casos de prueba**:

| Modo de Ejecución | Módulos Evaluados | Cantidad de Casos | Herramientas Utilizadas |
|---|---|:---:|---|
| **Automatizados** | Auth (5), Articles (9), Comments (3), Profiles (4), Favorites (3), Tags (2) | **26 Casos** | `pytest`, `pytest-asyncio`, `pytest-cov`, `HTTPX` |
| **Manuales** | Exploratorios (5), Herramientas (3), Calidad/Seguridad (4), Transición Estados (3) | **15 Casos** | `Swagger UI` (`/docs`), `Postman` (`postman.json`) |
| **TOTAL CONSOLIDADO** | **Todos los 19 endpoints de la especificación RealWorld** | **41 Casos** | **Cobertura de Requisitos: 100%** |

### 4.3 Técnicas de Diseño de Pruebas Dinámicas Aplicadas
1. **Partición de Equivalencia (Equivalence Partitioning - EP):**  
   División de los datos de entrada en clases válidas (deben ser aceptadas con 200/201) y clases inválidas (deben ser rechazadas con 400 o 422).  
   *Ejemplo:* Registro de usuarios con email válido vs. registro con email duplicado o sin formato arroba.
2. **Análisis de Valores Límite (Boundary Value Analysis - BVA):**  
   Evaluación de los extremos y bordes de las particiones.  
   *Ejemplo (CP-ART-A-009 y CP-EXP-M-004):* La regla de paginación establece que el límite por página por defecto es 20. Se evaluó enviar `?limit=100` para comprobar si la API acotaba el resultado al tope de 20 (falla detectada: BUG-09 entregó 25).
3. **Transición de Estados (State Transition Testing):**  
   Evaluación de máquinas de estado en relaciones dinámicas.  
   *Ejemplo:* Flujo de seguimiento de autores: No seguido (`following=false`) → Seguir (`following=true`) → Dejar de seguir (`following=false`).
4. **Pruebas de Seguridad y Control de Acceso (BOLA / IDOR Testing):**  
   Evaluación intencional de vectores de ataque donde un usuario intenta mutar o destruir recursos creados por otro usuario.

### 4.4 ¿Por qué 24 casos PASARON y 17 casos FALLARON?
* **En la rama `main` (limpia):** Pasan 26 de 26 pruebas automatizadas (**100% Pass**).
* **En la rama `buggy-version` (evaluada):** 
  * Casos que pasaron: **24 casos (58.54%)**.
  * Casos que fallaron: **17 casos (41.46%)**.
* **Explicación pedagógica vital:**  
  Que una prueba falle **no es un error del equipo de QA; es la prueba irrefutable de que el test fue diseñado con la sensibilidad suficiente para atrapar el defecto**. 9 de los casos fallaron directamente sobre las aserciones de los 9 bugs inyectados, y los otros 8 casos fallaron por efecto dominó o dependencia de estado (por ejemplo, al no poder seguir a un usuario, la prueba subsecuente de feed de seguidos también falla).

---

<div style="page-break-before: always;"></div>

# MÓDULO 5: RADIOGRAFÍA DE LOS 9 DEFECTOS DETECTADOS

A continuación se detalla la radiografía técnica y de negocio de los 9 bugs inyectados y detectados.

| Bug ID | Módulo | Severidad | Prioridad | Causa Raíz (Archivo y Línea) | Caso Detector | Impacto en el Negocio |
|---|---|:---:|:---:|---|---|---|
| **BUG-01** | `Auth` | **Baja** | Baja | `app/api/routes/authentication.py:22`<br>Falta `status_code=201` en decorador `@router.post`. | `CP-AUTH-A-001`<br>`CP-EXP-M-001` | Responde HTTP 200 en vez de 201 Created. Viola el estándar semántico REST pero el usuario sí se crea. |
| **BUG-02** | `Articles` | **Alta** | Alta | `app/schemas/article.py:21`<br>Falta `min_length=1` en `title: str`. | `CP-ART-A-002` | Permite crear artículos con título vacío (`""`), corrompiendo la persistencia y los feeds editoriales. |
| **BUG-03** | `Articles` | **Alta** | Alta | `app/api/routes/articles/articles.py:85`<br>Eliminada verificación de autoría en PUT. | `CP-ART-A-005`<br>`CP-QUAL-M-003` | **Falla BOLA:** Un usuario autenticado puede modificar el contenido de artículos creados por otros autores. |
| **BUG-04** | `Articles` | **Crítica** | **Alta** | `app/api/routes/articles/articles.py:112`<br>Eliminada verificación de autoría en DELETE. | `CP-ART-A-006`<br>`CP-QUAL-M-004` | **Brecha BOLA Crítica:** Cualquier usuario registrado puede borrar permanentemente artículos ajenos de la BD. |
| **BUG-05** | `Favorites` | **Alta** | Media | `app/api/routes/articles/articles.py:145`<br>Pasa `favorite=False` en vez de `True` al CRUD. | `CP-FAV-A-001`<br>`CP-EST-M-002` | Crash HTTP 500 no capturado (`ValueError: list.remove(x)`) al intentar marcar un artículo como favorito. |
| **BUG-06** | `Profiles` | **Media** | Media | `app/models/domain/users.py:48`<br>Hardcodeado `following=False` en DTO. | `CP-PRF-A-001`<br>`CP-EST-M-001` | La BD registra el seguimiento pero el JSON siempre responde `following: false`, desorientando al lector. |
| **BUG-07** | `Articles` | **Alta** | Alta | `app/api/routes/articles/articles.py:65`<br>Usa `OptionalCurrentUser` en feed privado. | `CP-ART-A-007` | Petición anónima a `/api/articles/feed` no da 401; colapsa con HTTP 500 por `NoneType.id`. |
| **BUG-08** | `Articles` | **Media** | Media | `app/crud/crud_article.py:52`<br>Comentada cláusula condicional de tag. | `CP-ART-A-008` | `GET /api/articles?tag=python` devuelve todos los artículos existentes ignorando el filtro temático. |
| **BUG-09** | `Articles` | **Media** | Media | `app/api/routes/articles/articles.py:35`<br>Eliminado `limit = min(limit, 20)`. | `CP-ART-A-009`<br>`CP-EXP-M-004` | Falla BVA: `?limit=100` devuelve 25 artículos en una sola carga en vez de acotar al tope máximo de 20. |

### 5.2 Análisis del Caso Crítico: BUG-04 (Vulnerabilidad OWASP BOLA)
Este es el defecto estrella del proyecto que justifica por sí solo el dictamen de aseguramiento de calidad:

* **¿Qué es BOLA?**  
  *Broken Object Level Authorization* (antes conocido como IDOR - *Insecure Direct Object Reference*). Es la vulnerabilidad número 1 del ranking internacional **OWASP API Security Top 10**.
* **El Fallo Técnico:**  
  El endpoint `DELETE /api/articles/{slug}` recibe el token de quien hace la petición (`current_user`), busca el artículo por su slug en la base de datos, pero **nunca compara si `article.author_id == current_user.id`**.
* **Demostración de Impacto:**  
  En Swagger UI, el usuario **Carlos** envió una petición DELETE contra el artículo publicado por **Laura**. El servidor respondió con `HTTP 200 OK` y borró físicamente el registro de la tabla `articles` en PostgreSQL.
* **Consecuencia de Negocio:**  
  Un atacante con un script de 10 líneas en bash o python puede recorrer todos los slugs y vaciar por completo la base de datos editorial de Conduit en cuestión de minutos.

---

# MÓDULO 6: GESTIÓN DE DEFECTOS EN GITHUB ISSUES

### 6.1 Transición Metodológica a GitHub Issues
Aunque originalmente se consideró MantisBT en la fase de planeación, el equipo adoptó **GitHub Issues** como la plataforma definitiva de gestión de incidencias. Esta decisión responde a las mejores prácticas de la industria contemporánea:
* Integración nativa con el repositorio y commits de Git (`Fixes #4`).
* Uso de sintaxis Markdown profesional enriquecida con bloques de código, tablas y alertas.
* Vinculación directa con el tablero Kanban de GitHub Projects.
* Estandarización mediante la plantilla oficial [`.github/ISSUE_TEMPLATE/bug_report.md`](../.github/ISSUE_TEMPLATE/bug_report.md).

### 6.2 Sistema de Etiquetas (Labels) Normalizado
Para permitir el filtrado y cálculo de métricas en GitHub Issues, se configuró una taxonomía precisa:

* **Tipo:** `bug`
* **Severidad:** `severity: critical`, `severity: high`, `severity: medium`, `severity: low`
* **Prioridad:** `priority: high`, `priority: medium`, `priority: low`
* **Módulo Afectado:** `module: auth`, `module: articles`, `module: favorites`, `module: profiles`
* **Estado:** `status: open`, `status: resolved`, `status: closed`

---

# MÓDULO 7: MÉTRICAS, INDICADORES Y EL DASHBOARD INTERACTIVO

### 7.1 Fórmulas Matemáticas y Resultados Cuantitativos

<div class="formula-box">
  <div class="formula-title">1. Cobertura de Ejecución de Pruebas</div>
  <div class="formula-math">Tasa de Ejecución = ( Casos Ejecutados ÷ Casos Planificados ) × 100</div>
  <div class="formula-calc"><strong>Cálculo:</strong> ( 41 ÷ 41 ) × 100 = <strong>100.0%</strong> &nbsp;|&nbsp; <em>Meta: ≥ 95% (Superada)</em></div>
</div>

<div class="formula-box">
  <div class="formula-title">2. Eficacia de Detección de Defectos (DRE - Defect Removal / Detection Effectiveness)</div>
  <div class="formula-math">DRE = [ Defectos Detectados en QA ÷ ( Defectos en QA + Defectos en Producción ) ] × 100</div>
  <div class="formula-calc"><strong>Cálculo:</strong> [ 9 ÷ ( 9 + 0 ) ] × 100 = <strong>100.0%</strong> &nbsp;|&nbsp; <em>Capacidad detectora perfecta</em></div>
</div>

<div class="formula-box">
  <div class="formula-title">3. Tasa de Aprobación de Casos en Rama de Evaluación</div>
  <div class="formula-math">Tasa de Aprobación = ( Casos Aprobados ÷ Casos Ejecutados Totales ) × 100</div>
  <div class="formula-calc"><strong>Cálculo:</strong> ( 24 ÷ 41 ) × 100 = <strong>58.54%</strong> &nbsp;|&nbsp; <em>24 Pasaron / 17 Fallaron cazando bugs</em></div>
</div>

<div class="formula-box">
  <div class="formula-title">4. Cobertura de Código Fuente (Statement Coverage con pytest-cov)</div>
  <div class="formula-math">Cobertura de Sentencias = ( Líneas Ejecutadas ÷ Líneas Totales ) × 100</div>
  <div class="formula-calc"><strong>Cálculo Global:</strong> ( 553 ÷ 668 ) × 100 = <strong>82.78%</strong> &nbsp;|&nbsp; <em>Meta: ≥ 70% (Superada)</em></div>
  <div class="formula-calc"><strong>Análisis Causa Raíz:</strong> Excluyendo el script CLI auxiliar <code>app/seed.py</code> (68 líneas sin transitar en HTTP), la cobertura real del servidor API en ejecución alcanza el <strong>92.17% (553 ÷ 600 sentencias)</strong>.</div>
</div>

<div class="formula-box">
  <div class="formula-title">5. Densidad de Defectos</div>
  <div class="formula-math">Densidad por Caso = Defectos Detectados ÷ Casos Ejecutados = 9 ÷ 41 = 0.220 defectos/caso</div>
  <div class="formula-math">Densidad por Mil Líneas (KLOC) = 9 defectos ÷ 0.668 KLOC = 13.47 defectos/KLOC</div>
</div>

<div class="formula-box">
  <div class="formula-title">6. Concentración de Defectos (Defect Clustering en Articles)</div>
  <div class="formula-math">Concentración = ( Defectos en Articles ÷ Defectos Totales ) × 100 = ( 6 ÷ 9 ) × 100 = 66.7%</div>
</div>

### 7.2 Arquitectura del Dashboard de Métricas (`dashboard_qa.html`)
El equipo construyó un tablero frontend profesional en HTML5, CSS moderno y JavaScript modular (sin dependencias de frameworks externos pesados), accesible directamente en [docs_qa/reports/dashboard_qa.html](reports/dashboard_qa.html).

* **Pestaña 1 (Resumen y Decisión):** Banner prominente del dictamen **NO-GO**, tarjetas KPI con indicadores visuales de meta y gráficos Donut en SVG nativo para ejecución y distribución de fallos.
* **Pestaña 2 (Ciclo de Métricas y Fórmulas):** Exposición de las fórmulas matemáticas paso a paso y alineación con las 5 fases del STLC.
* **Pestaña 3 (Cobertura y Suite Pytest):** Desglose de cobertura por capa arquitectónica (Modelos: 100%, Schemas: 100%, Core/DB: 97.37%, Rutas: 88.43%, Repositorios: 87.68%), inspector de archivos Python y verificador de integridad de datos (*Garbage in, garbage out*).
* **Pestaña 4 (Defectos y Casos):** Catálogo interactivo de los 41 casos y 9 defectos con buscador dinámico en tiempo real y modal visor de capturas de pantalla de evidencias.

---

# MÓDULO 8: ANÁLISIS DE CALIDAD Y FUNDAMENTACIÓN DEL DICTAMEN NO-GO

### 8.1 ¿Qué significa el Dictamen NO-GO?
En las organizaciones de software maduras, el equipo de Quality Assurance tiene la potestad de emitir una recomendación formal de salida (*Exit Criteria Review*):

* **GO (Autorizado):** El software cumple todos los criterios de calidad y puede desplegarse a producción.
* **NO-GO (Bloqueado):** El software contiene riesgos inadmisibles para el negocio que impiden su puesta en producción.

### 8.2 ¿Por qué se Bloquea el Pase si el 82.78% del Código está Cubierto?
Esta es una pregunta clásica de liderazgo en pruebas de software:
1. **La cobertura de código no mide corrección lógica:** Tener un 82% o 92% de cobertura solo indica que las líneas fueron transitadas por el intérprete, pero no garantiza que las líneas faltantes (como la guarda de autorización) no contengan omisiones fatales.
2. **Criterio de salida violado:** El Plan de Pruebas estableció taxativamente como Criterio de Éxito #2: **`0 defectos críticos abiertos al cierre`**.
3. **Existencia de BUG-04:** El defecto BUG-04 es una vulnerabilidad de severidad crítica abierta. Autorizar el pase a producción equivaldría a lanzar un sistema sabiendo que cualquier usuario anónimo o malintencionado puede destruir la información de todos los clientes.

---

# MÓDULO 9: GLOSARIO TÉCNICO MAESTRO (25+ CONCEPTOS CLAVE)

Aprende estas definiciones de memoria para responder con precisión quirúrgica en la sustentación:

1. **SUT (System Under Test):** El sistema o componente de software que está siendo sometido a evaluación de pruebas (en nuestro caso, la API de Conduit).
2. **Testware:** El conjunto de todos los artefactos, productos de trabajo y documentación generados durante el proceso de pruebas (plan de pruebas, casos de prueba, scripts pytest, evidencias, reportes de bugs, dashboard).
3. **BOLA (Broken Object Level Authorization):** Falla de seguridad en la que la API expone un endpoint que manipula un objeto específico mediante su identificador, pero no valida si el usuario solicitante tiene derechos de propiedad sobre dicho objeto.
4. **JWT (JSON Web Token):** Estándar abierto (RFC 7519) para transmitir de forma segura información autenticada en un objeto JSON compacto y firmado digitalmente.
5. **Slug:** Cadena de texto derivada del título de un artículo convertida en formato amigable para URLs (ej: "Mi Primer Post" → `mi-primer-post`), utilizada como identificador único en la API.
6. **Fixture de Pytest:** Función decorada con `@pytest.fixture` que provee datos, conexiones a base de datos o clientes HTTP configurados antes de que se ejecute un test, asegurando entornos limpios.
7. **AsyncClient (HTTPX):** Cliente HTTP asincrónico utilizado por pytest para enviar peticiones directas al ASGI de FastAPI sin necesidad de levantar un socket de red real en el sistema operativo.
8. **Assertion (Aserción):** Expresión booleana que verifica si una condición evaluada es verdadera. Si se evalúa como falsa, el test falla arrojando un `AssertionError`.
9. **Partición de Equivalencia (EP):** Técnica de caja negra que divide el dominio de datos en clases donde se asume que todos los valores producirán el mismo comportamiento en el sistema.
10. **Análisis de Valores Límite (BVA):** Técnica de caja negra que prueba los valores en los extremos, bordes o fronteras de las particiones de equivalencia (límite exacto, valor inmediatamente inferior y superior).
11. **Defect Clustering (Agrupamiento de Defectos):** Principio de ISTQB que postula que la gran mayoría de los defectos se concentran en una pequeña cantidad de módulos del software.
12. **Paradoja del Pesticida:** Principio de ISTQB que establece que repetir siempre los mismos casos de prueba disminuye su capacidad para encontrar defectos nuevos en el tiempo.
13. **DRE (Defect Removal/Detection Effectiveness):** Métrica porcentual que mide la capacidad del equipo de pruebas para detectar los defectos existentes antes de que el software llegue a los usuarios.
14. **Densidad de Defectos:** Relación matemática entre el número de defectos encontrados y el tamaño del software (medido en casos de prueba o líneas de código KLOC).
15. **Statement Coverage (Cobertura de Sentencias):** Métrica de caja blanca que calcula el porcentaje de sentencias ejecutables de código fuente que fueron transitadas por la suite de pruebas.
16. **Matriz RACI:** Herramienta de gestión que asigna roles para cada tarea del proyecto: Responsable (R), Aprobador (A), Consultado (C) e Informado (I).
17. **Criterios de Entrada (Entry Criteria):** Condiciones indispensables que deben cumplirse antes de iniciar formalmente una fase de pruebas (ej. ambiente levantado, base de datos migrada).
18. **Criterios de Salida (Exit Criteria):** Condiciones o umbrales de calidad que deben satisfacerse para dar por concluida una fase o autorizar el pase a producción.
19. **Smoke Test (Prueba de Humo):** Conjunto reducido de pruebas superficiales para verificar si las funciones más básicas del sistema operan antes de ejecutar pruebas exhaustivas.
20. **Prueba de Regresión:** Re-ejecución de pruebas para garantizar que los cambios recientes o parches de código no hayan roto funcionalidades que antes operaban correctamente.
21. **Prueba Exploratoria:** Enfoque de pruebas simultáneo donde el tester diseña, ejecuta y aprende sobre el sistema de manera iterativa sin guiones preestablecidos rígidos.
22. **Happy Path:** Ruta o flujo de ejecución ideal donde no ocurren condiciones de error ni excepciones y los datos provistos son 100% válidos.
23. **Negative Testing:** Pruebas diseñadas deliberadamente con datos inválidos, inesperados o maliciosos para comprobar la robustez y el manejo de excepciones de la aplicación.
24. **ASGI (Asynchronous Server Gateway Interface):** Estándar de interfaz en Python entre servidores web y aplicaciones asincrónicas, sucesor moderno de WSGI.
25. **Pydantic DTO (Data Transfer Object):** Esquemas que definen la estructura de datos que viaja en la red, realizando validación automática de tipos y serialización JSON.

---

<div style="page-break-before: always;"></div>

# MÓDULO 10: BANCO DE 10 PREGUNTAS TRAMPA DE LA DOCENTE Y CÓMO RESPONDERLAS

A continuación se presentan las 10 preguntas más exigentes que la docente puede formular durante la sustentación, junto con las respuestas senior argumentadas:

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 1: "Veo que tienen una tasa de aprobación de apenas 58.54% y 17 casos fallados. ¿Por qué su suite de pruebas tiene tantos fallos? ¿Está mal implementada?"</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    Profesora, esa tasa de fallos no es una debilidad de la suite; es la prueba de su éxito. En la rama limpia <code>main</code>, la misma suite de pruebas aprueba al 100% (26 de 26). En la rama <code>buggy-version</code>, inyectamos 9 defectos reales y diseñamos casos de prueba con la sensibilidad exacta para capturarlos. El 41.46% de fallos representa a nuestros tests cazando los bugs inyectados y detectando fallos en cadena. Un equipo de QA que reporte 100% de aprobación sobre un sistema defectuoso es un equipo que no está probando con profundidad.
  </div>
</div>

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 2: "Tienen una cobertura de código de 82.78%, que supera ampliamente la meta del 70%. ¿Por qué insisten en que el dictamen es NO-GO?"</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    Porque la cobertura de código mide cantidad de sentencias transitadas, no calidad ni corrección lógica. Nuestro criterio de salida número 2 establece de forma inviolable: <em>'0 defectos críticos abiertos al cierre'</em>. El defecto BUG-04 es una vulnerabilidad crítica de seguridad OWASP BOLA que permite que cualquier usuario registrado borre artículos ajenos de la base de datos. Autorizar un pase a producción con un bug crítico abierto viola las buenas prácticas de la industria y expondría a la empresa a un colapso reputacional y legal.
  </div>
</div>

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 3: "¿Cuál es la diferencia conceptual entre la severidad y la prioridad de un defecto en su proyecto? Denme un ejemplo."</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    La severidad es una métrica técnica intrínseca que evalúa el daño arquitectónico o estructural en el sistema. La prioridad es una métrica de gestión y negocio que evalúa la urgencia con la que debe repararse.<br>
    Por ejemplo, el BUG-01 (registro responde con código 200 en vez de 201) tiene Severidad Baja y Prioridad Baja porque el usuario sí se crea y el sistema sigue operando. En contraste, el BUG-04 tiene Severidad Crítica (pérdida de datos en PostgreSQL) y Prioridad Alta/Inmediata porque detiene por completo la viabilidad del negocio editorial.
  </div>
</div>

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 4: "¿Cómo aplicaron la técnica de Análisis de Valores Límite (BVA) en una API REST sin interfaz gráfica?"</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    La aplicamos sobre el endpoint de listado de artículos <code>GET /api/articles?limit=N</code>. La regla de negocio estipula que el sistema debe paginar con un límite máximo de 20 artículos por solicitud. Identificamos la frontera en 20. Diseñamos el caso automatizado <code>CP-ART-A-009</code> y el manual <code>CP-EXP-M-004</code> enviando un valor por encima del límite (<code>limit=100</code>) habiendo poblado la base con 25 artículos. El comportamiento esperado era que el backend acotara el resultado a un máximo de 20. El fallo detectado fue que la API devolvió los 25 registros en una sola carga, confirmando la ausencia de validación defensiva de frontera.
  </div>
</div>

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 5: "¿Por qué hicieron pruebas manuales si ya habían automatizado 26 casos en pytest?"</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    Porque la automatización y las pruebas manuales cumplen funciones complementarias según ISTQB. Pytest es ideal para pruebas de regresión, verificación rápida de contratos HTTP y cobertura continua. Sin embargo, las 15 pruebas manuales en Swagger UI y Postman nos permitieron realizar pruebas exploratorias, verificar la claridad de la documentación para desarrolladores externos, manipular tokens JWT corruptos y simular con realismo flujos complejos entre dos usuarios simultáneos (como Carlos intentando modificar o borrar el post de Laura), capturando evidencias fotográficas visuales directas.
  </div>
</div>

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 6: "¿Qué es la vulnerabilidad BOLA y por qué se considera un riesgo de negocio y no solo un fallo técnico?"</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    BOLA significa <em>Broken Object Level Authorization</em> (Vulnerabilidad #1 en OWASP API Security). Ocurre cuando la API valida quién es el usuario pero no valida si ese usuario es dueño del recurso que intenta modificar o borrar. En Conduit, el endpoint DELETE recibía el token de Carlos y borraba el artículo de Laura. Es un riesgo de negocio crítico porque en una plataforma de blogs, si un autor no puede confiar en que sus publicaciones están protegidas, la plataforma sufre desbandada de creadores y demandas por pérdida de propiedad intelectual.
  </div>
</div>

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 7: "¿Cómo demostraron el principio de Agrupamiento de Defectos (Defect Clustering) en su taller?"</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    El principio 4 de ISTQB establece que la mayoría de los defectos se concentran en un número reducido de módulos. En nuestro proyecto, de los 9 defectos inyectados y detectados, 6 se localizaron en el módulo Articles (66.7% de concentración). Esto es coherente con el negocio, ya que Articles es el módulo con mayor complejidad ciclomática: maneja filtrado por tags, feeds privados, paginación, edición, borrado y persistencia de autoría.
  </div>
</div>

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 8: "En el reporte de cobertura dicen que pytest-cov marcó 82.78%, pero ustedes afirman que en realidad la API tuvo 92.17%. ¿Están maquillando las métricas?"</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    No, estamos haciendo un análisis de causa raíz transparente. El archivo <code>app/seed.py</code> tiene 68 líneas de código que representan un script auxiliar de consola (CLI) para poblar datos de prueba iniciales. Este archivo no forma parte del flujo de ejecución del servidor web en tiempo de ejecución. Al calcular 553 sentencias ejecutadas entre 600 sentencias de la API real, la cobertura efectiva es del 92.17%. En el dashboard mostramos ambas cifras con total transparencia para que el revisor técnico conozca el desglose exacto.
  </div>
</div>

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 9: "Si los desarrolladores corrigen los 9 bugs hoy, ¿qué harían ustedes mañana como equipo de QA?"</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    Ejecutaríamos tres pasos formales del STLC:<br>
    1. <strong>Re-testing (Confirmación de corrección):</strong> Ejecutar los 9 casos específicos que fallaron para certificar que ahora aprueban.<br>
    2. <strong>Pruebas de Regresión Completa:</strong> Correr la suite automatizada completa de 26 casos y los flujos manuales para asegurar que las correcciones no introdujeron nuevos defectos colaterales.<br>
    3. <strong>Revisión de Criterios de Salida y Cambio de Dictamen:</strong> Si los 9 bugs están cerrados y no hay defectos críticos abiertos, emitimos el informe final de cierre y cambiamos el dictamen a <strong>GO (Aprobado para Producción)</strong>.
  </div>
</div>

<div class="qa-item">
  <div class="qa-q">❓ Pregunta 10: "¿Cómo se dividieron el trabajo entre Juan Pablo y Niurka? ¿Fue un trabajo individual o en equipo?"</div>
  <div class="qa-a">
    <strong>💡 Respuesta Senior:</strong><br>
    Trabajamos como una célula de calidad bajo la Matriz RACI documentada en el Plan de Pruebas:
    <ul style="margin: 6px 0 6px 18px; padding: 0;">
      <li><strong>Juan Pablo:</strong> Lideró la arquitectura de pruebas, el diseño y desarrollo de los 26 scripts automatizados en <code>pytest</code>, la configuración del entorno Docker/PostgreSQL, las pruebas de seguridad con JWT y la generación de métricas de cobertura.</li>
      <li><strong>Niurka:</strong> Lideró la co-estructuración del Plan de Pruebas maestro, la ejecución de las pruebas manuales en Swagger UI y Postman, la clasificación de los 9 defectos en GitHub Issues con la captura de evidencias fotográficas, el co-diseño del dashboard y la redacción del informe de análisis de calidad.</li>
    </ul>
    Ambos colaboramos en el diseño de los 41 casos y en la interpretación del modelo de negocio.
  </div>
</div>

---

<div style="page-break-before: always;"></div>

# MÓDULO 11: ESTRUCTURA SUGERIDA DE EXPOSICIÓN ORAL Y GUION DE DEFENSA

> ### 🎯 GUÍA MAESTRA DE DEFENSA ANTE LA DOCENTE (12 A 15 MINUTOS)
> Este guion está diseñado para proyectar solidez técnica, dominio del negocio y liderazgo senior en aseguramiento de calidad. Utilicen la distribución de roles acordada en la Matriz RACI.

### 11.1 Planificación Minuto a Minuto y Diapositivas Recomendadas

```text
  [00:00 - 02:00]  DIAPOSITIVAS 1 & 2: INTRODUCCIÓN Y CONTEXTO DE NEGOCIO (Niurka)
  [02:00 - 05:00]  DIAPOSITIVAS 3 & 4: ESTRATEGIA STLC Y CATÁLOGO DE CASOS (Juan Pablo)
  [05:00 - 08:30]  DIAPOSITIVA 5: DEFECTOS EN GITHUB Y BRECHA CRÍTICA BOLA (Niurka)
  [08:30 - 11:30]  DIAPOSITIVA 6: DEMO EN VIVO DEL DASHBOARD Y MÉTRICAS (Juan Pablo)
  [11:30 - 13:00]  DIAPOSITIVA 7: DICTAMEN NO-GO Y PLAN DE REMEDIACIÓN (Ambos)
  [13:00 - 15:00]  DIAPOSITIVA 8: RONDA DE PREGUNTAS Y CIERRE (Ambos)
```

---

### 11.2 Guion Detallado de Intervención por Expositor

#### 🎙️ Acto 1: Introducción y Modelo de Negocio (Minuto 0:00 a 2:00) — *Expone: Niurka Mejía*
* **Qué proyectar:** Portada y Diapositiva del Contexto del Negocio Conduit (Medium clone).
* **Guion sugerido:**
  > *"Buenas tardes, profesora Yury. Hoy presentamos los resultados del ciclo de aseguramiento de calidad sobre la API Conduit, implementada en FastAPI con PostgreSQL.  
  > Queremos iniciar con una premisa fundamental de su clase: el testing no se hace en el vacío; se rige por el modelo de negocio. Conduit es una plataforma editorial abierta donde los usuarios publican artículos y construyen reputación. En este ecosistema, la autoría y la privacidad no son simples atributos funcionales: son el activo vital de la compañía. Si un autor no puede confiar en que sus publicaciones están protegidas, la plataforma fracasa. Por ello, nuestra estrategia no solo evaluó si los endpoints responden 200 OK, sino si garantizan la integridad del negocio."*

#### 🎙️ Acto 2: Estrategia STLC y Diseño de Casos (Minuto 2:00 a 5:00) — *Expone: Juan Pablo Velásquez*
* **Qué proyectar:** Diagrama de las 5 fases del STLC y Pirámide de Pruebas (26 automatizadas + 15 manuales).
* **Guion sugerido:**
  > *"Gracias, Niurka. Para abordar el sistema implementamos las 5 fases del Software Testing Life Cycle (STLC). Diseñamos un total de 41 casos de prueba, superando la meta de 40.  
  > Aplicamos una arquitectura de pruebas equilibrada:  
  > 1. En la base, 26 casos automatizados en pytest con soporte asincrónico mediante HTTPX y bases de datos transaccionales en Docker, logrando un 82.78% de cobertura de código.  
  > 2. En la capa superior, 15 casos manuales ejecutados en Swagger UI y Postman, aplicando Partición de Equivalencia, Análisis de Valores Límite (BVA) y pruebas de seguridad.  
  > Un aspecto clave de nuestra metodología fue el uso de dos ramas en Git: la rama 'main' donde el 100% de los tests aprueban para verificar que no hay falsos positivos, y la rama 'buggy-version' donde evaluamos la capacidad de la suite frente a 9 defectos reales."*

#### 🎙️ Acto 3: Gestión de Defectos y Hallazgo Crítico BOLA (Minuto 5:00 a 8:30) — *Expone: Niurka Mejía*
* **Qué proyectar:** Reporte de GitHub Issues y la captura de pantalla de la evidencia de **BUG-04**.
* **Guion sugerido:**
  > *"En la fase de ejecución detectamos los 9 defectos inyectados, alcanzando una Eficacia Detectora (DRE) del 100%. Para su gestión, adoptamos GitHub Issues mediante una plantilla basada estrictamente en la taxonomía de clase: Error Humano, Defecto en Código y Fallo Observable.  
  > Además, confirmamos el Principio 4 de ISTQB: Agrupamiento de Defectos. El 66.7% de los bugs se concentraron en el módulo Articles.  
  > Queremos llamar la atención sobre el hallazgo más grave: el BUG-04. Se trata de una falla de autorización BOLA, clasificada como la amenaza número 1 por OWASP API Security. Demostramos cómo el usuario Carlos, enviando una petición DELETE con su propio token, logró eliminar permanentemente el artículo de Laura de la base de datos sin recibir ninguna restricción de autoría."*

#### 🎙️ Acto 4: Demostración en Vivo del Dashboard y Métricas (Minuto 8:30 a 11:30) — *Expone: Juan Pablo Velásquez*
* **Qué proyectar:** Tablero interactivo [dashboard_qa.html](reports/dashboard_qa.html) en el navegador.
* **Guion sugerido:**
  > *"Para presentar la visibilidad ejecutiva a los stakeholders, desarrollamos este Dashboard interactivo de 4 pestañas.  
  > Como pueden observar en la Pestaña 1, la suite ejecutó el 100% de los casos previstos. La tasa de aprobación en esta rama fue del 58.54%, lo que refleja a nuestras pruebas atrapando exitosamente las anomalías.  
  > En la Pestaña 3 mostramos la cobertura por capa: Modelos y Schemas al 100%, Core y Rutas por encima del 88%.  
  > Sin embargo, como verán en el encabezado principal, el dictamen formal es NO-GO. A pesar de una cobertura excelente del 82.78%, nuestro criterio de salida exige cero defectos críticos abiertos. Con el BUG-04 sin resolver, el software no es apto para producción."*

#### 🎙️ Acto 5: Conclusiones y Plan de Remediación (Minuto 11:30 a 13:00) — *Exponen: Ambos*
* **Qué proyectar:** Hoja de Ruta de Remediación y diapositiva de conclusiones.
* **Guion sugerido:**
  > *Niurka:* *"El rol de QA no es dar aprobaciones complacientes, sino salvaguardar el negocio. Este taller demostró que una prueba superficial hubiera aprobado el sistema porque los endpoints responden rápido, pero una estrategia rigurosa salvó a la empresa de una catástrofe de seguridad."*  
  > *Juan Pablo:* *"El plan de acción inmediato consiste en: aplicar la guarda de autorización en articles.py, corregir la inversión booleana en favoritos, ejecutar pruebas de regresión completa y, una vez confirmados los parches, proceder con el cambio de dictamen a GO. Quedamos atentos a sus preguntas."*

---

### 11.3 Recomendaciones Finales de Oratoria y Postura
1. **Seguridad y compostura:** Hablen con propiedad de "nuestros casos de prueba", "nuestra suite de pytest" y "nuestro criterio de salida".
2. **Defiendan el NO-GO con orgullo:** Los evaluadores universitarios suelen esperar que los estudiantes digan que todo está perfecto. Decir "el software está bloqueado por NO-GO" fundamentado en OWASP BOLA demuestra una madurez profesional que los distinguirá de inmediato.
3. **Manejo del Dashboard:** Abran el archivo HTML localmente antes de iniciar la presentación; muestren cómo cambian los filtros y cómo se previsualizan las evidencias fotográficas al hacer clic en los defectos.

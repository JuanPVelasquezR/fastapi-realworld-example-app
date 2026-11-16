# Reporte de Defectos (Bugs) — GitHub Issues
## Proyecto: FastAPI RealWorld Example App (Conduit API)
### Entorno: Ejecución contra rama `buggy-version` (Python 3.14 + PostgreSQL en Docker)
**Equipo QA:** Juan Pablo Velásquez Ramírez (QA Lead & Automatizador) & Niurka Liseth Mejía Vargas (QA Analyst & Bug Manager)  
**Supervisión Académica:** Yury Montoya P. — Pruebas de Software  
**Plataforma de Seguimiento de Defectos:** **GitHub Issues** (Repositorio del Proyecto)  
**Plantilla Base:** `.github/ISSUE_TEMPLATE/bug_report.md`  

---

## 📑 1. Marco Metodológico y Taxonomía de Defectos

El presente reporte consolida los **9 defectos reales** detectados durante el ciclo de pruebas dinámicas (26 pruebas automatizadas en `pytest` y 15 pruebas manuales en `Swagger UI / Postman`), gestionados formalmente a través de **GitHub Issues** mediante etiquetas normalizadas (*labels*), hitos (*milestones*) y asignaciones cruzadas.

### 1.1 Cadena Causal ISTQB (§2.1 de los Fundamentos de Calidad)
Cada incidencia reportada en este catálogo se estructura rigurosamente distinguiendo los tres eslabones causales de la calidad de software:
1. **Error Humano:** Acción equivocada realizada por el desarrollador durante la arquitectura, diseño o codificación.
2. **Defecto en Código (Bug / Causa Raíz):** Manifestación estática en el código fuente (archivo, función, línea) que contiene la imperfección.
3. **Fallo Observable Dinámico:** Desviación externa en tiempo de ejecución observable por el cliente o la suite de pruebas (código HTTP erróneo, caída del servidor, alteración ilegítima de datos).

### 1.2 Severidad Técnica vs. Prioridad de Negocio (§2.2)
* **Severidad (Métrica Técnica Objetiva):** Evalúa la gravedad intrínseca del impacto sobre la integridad de datos, la arquitectura y la estabilidad del backend (`Crítica`, `Alta`, `Media`, `Baja`).
* **Prioridad (Métrica de Gestión de Negocio):** Evalúa la urgencia cronológica de corrección considerando el impacto sobre el modelo de negocio de Conduit como **plataforma de publicaciones y blogs tipo Medium** (`Alta`, `Media`, `Baja`).

### 1.3 Sistema de Etiquetas (Labels) en GitHub Issues
Para la administración, filtrado y trazabilidad de los defectos en GitHub Issues, se definió la siguiente taxonomía de etiquetas:

| Categoría | Etiquetas de GitHub | Propósito |
|---|---|---|
| **Tipo** | `bug` | Clasificación del issue como defecto de software |
| **Severidad Técnica** | `severity: critical`, `severity: high`, `severity: medium`, `severity: low` | Nivel de impacto arquitectónico y sistémico |
| **Prioridad de Negocio** | `priority: high`, `priority: medium`, `priority: low` | Urgencia de corrección para el negocio editorial |
| **Módulo Afectado** | `module: auth`, `module: articles`, `module: profiles`, `module: favorites` | Agrupamiento funcional (Principio 4 ISTQB) |
| **Estado de Ciclo** | `status: open`, `status: in-progress`, `status: resolved`, `status: closed` | Estado en el flujo de trabajo de resolución |

---

## 📊 2. Matriz Resumen de Defectos (Defect Clustering)

> **Principio 4 ISTQB — Agrupamiento de Defectos (*Defect Clustering*):**  
> El 66.7% de las anomalías detectadas (6 de 9 defectos) se concentran en el módulo crítico de **Articles**, el cual gestiona la persistencia, autoría y publicación de contenidos, confirmando la concentración no uniforme de fallos en componentes neurálgicos.

| Issue | Defecto ID | Módulo | Título Resumido | Severidad | Prioridad | Caso(s) Asociado(s) | Estado en GitHub |
|---|---|---|---|---|---|---|---|
| **#1** | **BUG-01** | `Auth` | Registro exitoso retorna HTTP 200 en lugar de HTTP 201 Created | `Baja` | `Baja` | `CP-AUTH-A-001`, `CP-EXP-M-001` | `status: open` |
| **#2** | **BUG-02** | `Articles` | Permite crear artículos con título vacío (`""`) sin validación | `Alta` | `Alta` | `CP-ART-A-002` | `status: open` |
| **#3** | **BUG-03** | `Articles` | Falla de Autorización (BOLA): Edición de artículos de otros autores | `Alta` | `Alta` | `CP-ART-A-005`, `CP-QUAL-M-003` | `status: open` |
| **#4** | **BUG-04** | `Articles` | **Brecha Crítica (BOLA): Eliminación arbitraria de artículos ajenos** | **`Crítica`** | **`Alta`** | `CP-ART-A-006`, `CP-QUAL-M-004` | `status: open` *(Bloqueante)* |
| **#5** | **BUG-05** | `Favorites` | Inversión de lógica booleana en favoritos causa HTTP 500 (`ValueError`) | `Alta` | `Media` | `CP-FAV-A-001`, `CP-FAV-A-002`, `CP-EST-M-002` | `status: open` |
| **#6** | **BUG-06** | `Profiles` | Estado de seguimiento `following` siempre retorna `false` en duro | `Media` | `Media` | `CP-PRF-A-001`, `CP-PRF-A-002`, `CP-EST-M-001` | `status: open` |
| **#7** | **BUG-07** | `Articles` | Feed personal `/api/articles/feed` accesible sin auth causa crash 500 | `Alta` | `Alta` | `CP-ART-A-007` | `status: open` |
| **#8** | **BUG-08** | `Articles` | Filtro por etiqueta `?tag=...` es ignorado devolviendo catálogo total | `Media` | `Media` | `CP-ART-A-008` | `status: open` |
| **#9** | **BUG-09** | `Articles` | Parámetro `?limit=100` excede el tope de 20 artículos (Falla BVA) | `Media` | `Media` | `CP-ART-A-009`, `CP-EXP-M-004` | `status: open` |

---

## 🗂️ 3. Fichas de Reporte de Defectos (GitHub Issues)

---

### Issue #1: [BUG-01] POST /api/users retorna HTTP 200 en lugar de 201 Created al registrar un usuario

#### 📋 Metadatos del Defecto
* **Identificador:** `BUG-01`
* **Módulo Afectado:** `Auth` (Autenticación y Registro)
* **Caso(s) de Prueba Asociado(s):** [CP-AUTH-A-001](Casos_De_Prueba.md#cp-auth-a-001) *(pytest)*, [CP-EXP-M-001](Casos_De_Prueba.md#cp-exp-m-001) *(Swagger UI)*
* **Severidad Técnica:** `Baja`
* **Prioridad de Negocio:** `Baja`
* **Estado en GitHub:** `[x] Abierto (Open)`
* **Etiquetas (Labels):** `bug`, `module: auth`, `severity: low`, `priority: low`, `status: open`
* **Reportado por:** Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas
* **Fecha de Reporte:** 09/11/2026
* **Asignado a:** Niurka Liseth Mejía Vargas (Issue Tracking) / Dev Team

#### 🧬 Cadena Causal ISTQB
* **Error Humano:** El desarrollador omitió declarar el código semántico de estado en el decorador de ruta de FastAPI, asumiendo el valor predeterminado del framework (`200 OK`).
* **Defecto en Código (Causa Raíz):** En `app/api/routes/authentication.py`, línea 22, el decorador `@router.post("/users", response_model=UserInResponse)` carece de la propiedad `status_code=status.HTTP_201_CREATED`.
* **Fallo Dinámico Observable:** Al registrar un nuevo usuario con payload válido, la API responde con cabecera `HTTP/1.1 200 OK` en lugar de `HTTP/1.1 201 Created`.

#### 💼 Justificación de Impacto en el Negocio
* **Impacto en el Negocio:** No bloquea la operativa de la plataforma (el usuario se registra y el JWT se genera), pero vulnera las directrices de la especificación RealWorld y estándares RESTful (RFC 7231 §4.3.3), impidiendo que clientes móviles o integraciones frontend distingan formalmente entre creación de recursos y lecturas idempotentes.
* **Severidad:** Baja (sin corrupción ni indisponibilidad).
* **Prioridad:** Baja (puede programarse para el siguiente sprint sin detener la entrega).

#### ⚙️ Precondiciones y Datos de Prueba
* Base de datos PostgreSQL levantada y accesible.
* Cuenta de prueba con email y username no existentes previamente en la base de datos.

#### 🔁 Pasos para Reproducir
1. Enviar una petición HTTP POST a `http://localhost:8000/api/users`.
2. Incluir el header `Content-Type: application/json`.
3. Enviar el siguiente cuerpo en formato JSON:
```json
{
  "user": {
    "username": "usuario_prueba_01",
    "email": "usuario_prueba_01@test.com",
    "password": "password123"
  }
}
```
4. Inspeccionar el código de estado retornado en las cabeceras HTTP.

#### 🎯 Comportamiento Esperado vs. Obtenido
* **Resultado Esperado:** `HTTP 201 Created`. Objeto JSON con datos del usuario creado y token JWT correspondiente.
* **Resultado Obtenido:** `HTTP 200 OK`. Objeto JSON devuelto correctamente, pero con código de estado 200.

#### 📸 Evidencias Técnicas
* **Evidencia Automatizada (pytest):**
```text
FAILED tests/test_auth.py::test_registro_retorna_201 - AssertionError: [CP-AUTH-A-001] Se esperaba HTTP 201, se obtuvo 200.
```
* **Evidencia Manual (Swagger UI):**
Captura de pantalla: [docs_qa/evidencias/CP-EXP-M-001_registro- Codigo 200 Error Creacion de Usuario.png](evidencias/CP-EXP-M-001_registro-%20Codigo%20200%20Error%20Creacion%20de%20Usuario.png)

![Evidencia BUG-01](evidencias/CP-EXP-M-001_registro-%20Codigo%20200%20Error%20Creacion%20de%20Usuario.png)

#### 🛡️ Criterios de Cierre y Verificación
- [ ] Incorporar `status_code=status.HTTP_201_CREATED` en el decorador de `@router.post("/users")`.
- [ ] Ejecución exitosa de `pytest tests/test_auth.py::test_registro_retorna_201` (`PASSED`).

---

### Issue #2: [BUG-02] Esquema de creación de artículos permite títulos vacíos ("") sin validación

#### 📋 Metadatos del Defecto
* **Identificador:** `BUG-02`
* **Módulo Afectado:** `Articles` (Esquemas de Entrada y Persistencia)
* **Caso(s) de Prueba Asociado(s):** [CP-ART-A-002](Casos_De_Prueba.md#cp-art-a-002) *(pytest)*
* **Severidad Técnica:** `Alta`
* **Prioridad de Negocio:** `Alta`
* **Estado en GitHub:** `[x] Abierto (Open)`
* **Etiquetas (Labels):** `bug`, `module: articles`, `severity: high`, `priority: high`, `status: open`
* **Reportado por:** Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas
* **Fecha de Reporte:** 09/11/2026
* **Asignado a:** Niurka Liseth Mejía Vargas (Issue Tracking) / Dev Team

#### 🧬 Cadena Causal ISTQB
* **Error Humano:** El desarrollador definió el campo `title` en el modelo Pydantic como `str` genérico sin adjuntar la restricción de longitud mínima `min_length=1`.
* **Defecto en Código (Causa Raíz):** En `app/schemas/article.py`, clase `NewArticle`, el atributo `title: str` no cuenta con `Field(..., min_length=1)`.
* **Fallo Dinámico Observable:** Al invocar `POST /api/articles` con `{"title": ""}`, la capa de validación no intercepta la anomalía y genera un artículo con título vacío en PostgreSQL con respuesta `HTTP 200 OK` en vez de `HTTP 422 Unprocessable Entity`.

#### 💼 Justificación de Impacto en el Negocio
* **Impacto en el Negocio:** En una plataforma de publicaciones editoriales (tipo Medium), los artículos sin título generan corrupción en el feed público, inconsistencias visuales en el frontend y slugs vacíos o inválidos (`/api/articles/`), imposibilitando que los lectores naveguen o compartan el contenido.
* **Severidad:** Alta (degradación de integridad de datos en la base de datos).
* **Prioridad:** Alta (debe corregirse con presteza para salvaguardar la experiencia de lectura).

#### ⚙️ Precondiciones y Datos de Prueba
* Usuario registrado y autenticado en la plataforma.
* Token JWT válido obtenido mediante login.

#### 🔁 Pasos para Reproducir
1. Autenticarse como usuario para obtener el token Bearer.
2. Enviar petición HTTP POST a `http://localhost:8000/api/articles`.
3. Headers:
```http
Authorization: Bearer <token_jwt>
Content-Type: application/json
```
4. Body JSON:
```json
{
  "article": {
    "title": "",
    "description": "Prueba de publicación sin título",
    "body": "Cuerpo del artículo de prueba",
    "tagList": []
  }
}
```
5. Observar el código HTTP retornado y el registro creado en BD.

#### 🎯 Comportamiento Esperado vs. Obtenido
* **Resultado Esperado:** `HTTP 422 Unprocessable Entity`. La API debe rechazar el payload indicando que el campo `title` debe contener al menos 1 caracter no vacío.
* **Resultado Obtenido:** `HTTP 200 OK`. El servidor acepta el artículo y persiste en BD un registro con `title: ""` y slug anómalo.

#### 📸 Evidencias Técnicas
* **Evidencia Automatizada (pytest):**
```text
FAILED tests/test_articles.py::test_crear_articulo_titulo_vacio_retorna_422 - AssertionError: [CP-ART-A-002] Se esperaba HTTP 422, se obtuvo 200.
```
* **Reporte HTML:** [docs_qa/reports/test_report.html](reports/test_report.html)

#### 🛡️ Criterios de Cierre y Verificación
- [ ] Aplicar restricción `title: str = Field(..., min_length=1)` en `NewArticle` (`app/schemas/article.py`).
- [ ] Ejecución exitosa de `pytest tests/test_articles.py::test_crear_articulo_titulo_vacio_retorna_422` (`PASSED`).

---

### Issue #3: [BUG-03] Falla de Autorización (BOLA): Cualquier usuario autenticado puede modificar artículos de otros autores

#### 📋 Metadatos del Defecto
* **Identificador:** `BUG-03`
* **Módulo Afectado:** `Articles` (Control de Acceso y Autorización)
* **Caso(s) de Prueba Asociado(s):** [CP-ART-A-005](Casos_De_Prueba.md#cp-art-a-005) *(pytest)*, [CP-QUAL-M-003](Casos_De_Prueba.md#cp-qual-m-003) *(Swagger UI)*
* **Severidad Técnica:** `Alta`
* **Prioridad de Negocio:** `Alta`
* **Estado en GitHub:** `[x] Abierto (Open)`
* **Etiquetas (Labels):** `bug`, `security`, `module: articles`, `severity: high`, `priority: high`, `status: open`
* **Reportado por:** Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas
* **Fecha de Reporte:** 09/11/2026
* **Asignado a:** Niurka Liseth Mejía Vargas (Issue Tracking) / Dev Team

#### 🧬 Cadena Causal ISTQB
* **Error Humano:** El desarrollador suprimió la cláusula condicional de verificación de autoría en la función controladora de actualización de artículos.
* **Defecto en Código (Causa Raíz):** En `app/api/routes/articles/articles.py`, endpoint `update_article_by_slug`, se eliminó la instrucción:
  ```python
  if article.author_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not the author of this article")
  ```
* **Fallo Dinámico Observable:** Un usuario B autenticado puede enviar un PUT sobre un slug creado por el usuario A y la API procesa la mutación exitosamente respondiendo `HTTP 200 OK`.

#### 💼 Justificación de Impacto en el Negocio
* **Impacto en el Negocio:** Vulnerabilidad directa clasificada en OWASP API Security Top 10 como **API1:2023 Broken Object Level Authorization (BOLA)**. En un portal de noticias o blogs, destruye la confiabilidad: cualquier usuario puede adulterar textos ajenos, suplantar la voz editorial de autores reconocidos o inyectar contenido inapropiado.
* **Severidad:** Alta (violación estructural de control de acceso e integridad).
* **Prioridad:** Alta (urgencia máxima previa a cualquier despliegue público).

#### ⚙️ Precondiciones y Datos de Prueba
* Usuario A registrado con artículo existente: `slug: articulo-autor-a`.
* Usuario B registrado y autenticado con su propio token JWT.

#### 🔁 Pasos para Reproducir
1. Autenticarse como Usuario B (atacante) y obtener su token Bearer.
2. Enviar petición HTTP PUT a `http://localhost:8000/api/articles/articulo-autor-a`.
3. Headers:
```http
Authorization: Bearer <token_usuario_b>
Content-Type: application/json
```
4. Body JSON:
```json
{
  "article": {
    "title": "Contenido Adulterado por Usuario B",
    "body": "Texto modificado de forma maliciosa"
  }
}
```
5. Consultar el artículo en base de datos o mediante GET.

#### 🎯 Comportamiento Esperado vs. Obtenido
* **Resultado Esperado:** `HTTP 400 Bad Request` (o `HTTP 403 Forbidden`). Mensaje descriptivo de rechazo de autorización; el artículo permanece inalterado.
* **Resultado Obtenido:** `HTTP 200 OK`. El servidor actualiza el artículo del Usuario A con los datos provistos por el Usuario B.

#### 📸 Evidencias Técnicas
* **Evidencia Automatizada (pytest):**
```text
FAILED tests/test_articles.py::test_editar_articulo_ajeno_retorna_400 - AssertionError: [CP-ART-A-005] Se esperaba HTTP 400, se obtuvo 200. Posible BUG-03: la verificación de autoría en PUT fue eliminada.
```
* **Evidencia Manual (Swagger UI):**
Captura de pantalla: [docs_qa/evidencias/P-QUAL-M-003_edit_ajeno_bug03.png](evidencias/P-QUAL-M-003_edit_ajeno_bug03.png)  
*(El usuario Carlos modifica exitosamente el artículo perteneciente a Laura recibiendo 200 OK)*.

![Evidencia BUG-03](evidencias/P-QUAL-M-003_edit_ajeno_bug03.png)

#### 🛡️ Criterios de Cierre y Verificación
- [ ] Reincorporar la validación estricta de autoría `article.author_id == current_user.id` en `update_article_by_slug`.
- [ ] Ejecución exitosa de `pytest tests/test_articles.py::test_editar_articulo_ajeno_retorna_400` (`PASSED`).

---

### Issue #4: [BUG-04] BRECHA CRÍTICA DE SEGURIDAD (OWASP BOLA): Cualquier usuario autenticado puede eliminar permanentemente artículos ajenos

#### 📋 Metadatos del Defecto
* **Identificador:** `BUG-04`
* **Módulo Afectado:** `Articles` (Control de Acceso y Operaciones Destructivas)
* **Caso(s) de Prueba Asociado(s):** [CP-ART-A-006](Casos_De_Prueba.md#cp-art-a-006) *(pytest)*, [CP-QUAL-M-004](Casos_De_Prueba.md#cp-qual-m-004) *(Swagger UI)*
* **Severidad Técnica:** **`Crítica`**
* **Prioridad de Negocio:** **`Alta` (Bloqueante de Pase a Producción / NO-GO)**
* **Estado en GitHub:** `[x] Abierto (Open)`
* **Etiquetas (Labels):** `bug`, `security`, `blocker`, `severity: critical`, `priority: high`, `status: open`
* **Reportado por:** Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas
* **Fecha de Reporte:** 09/11/2026
* **Asignado a:** Niurka Liseth Mejía Vargas (Issue Tracking) / Dev Team

#### 🧬 Cadena Causal ISTQB
* **Error Humano:** Omisión absoluta de la validación de propiedad del recurso en la ruta de eliminación física de registros.
* **Defecto en Código (Causa Raíz):** En `app/api/routes/articles/articles.py`, endpoint `delete_article_by_slug`, el controlador recibe `current_user` pero no verifica la igualdad entre `article.author_id` y `current_user.id`, ejecutando directamente `crud_article.delete_article(...)`.
* **Fallo Dinámico Observable:** Una petición DELETE a `/api/articles/{slug}` enviada por cualquier usuario registrado elimina irreversiblemente el artículo de la base de datos PostgreSQL, respondiendo `HTTP 200 OK` (o `204 No Content`).

#### 💼 Justificación de Impacto en el Negocio
* **Impacto en el Negocio:** Catastrófico. Constituye un fallo directo de seguridad OWASP BOLA que permite un ataque de denegación de servicio de contenidos (*content wipeout*). Cualquier atacante con una cuenta básica puede ejecutar un bucle destructivo y vaciar todos los artículos publicados en la plataforma en minutos, causando pérdida patrimonial de datos e insolvencia reputacional.
* **Severidad:** **Crítica** (Pérdida irreversible de datos primarios en el sistema).
* **Prioridad:** **Alta / Inmediata** (Criterio de parada del STLC: no se puede autorizar el pase a producción con este defecto abierto).

#### ⚙️ Precondiciones y Datos de Prueba
* Usuario A (propietario) con un artículo publicado en base de datos.
* Usuario B (atacante) con cuenta activa y token Bearer válido.

#### 🔁 Pasos para Reproducir
1. Autenticar a Usuario B en Swagger UI o mediante Postman.
2. Configurar una petición HTTP DELETE apuntando a `http://localhost:8000/api/articles/{slug_de_usuario_a}`.
3. Incluir cabecera `Authorization: Bearer <token_usuario_b>`.
4. Ejecutar la solicitud.
5. Realizar una petición GET sobre el mismo slug o revisar la tabla `articles` en PostgreSQL.

#### 🎯 Comportamiento Esperado vs. Obtenido
* **Resultado Esperado:** `HTTP 400 Bad Request` (o `HTTP 403 Forbidden`). El sistema debe bloquear la eliminación y preservar el registro intacto en la base de datos.
* **Resultado Obtenido:** `HTTP 200 OK`. El servidor borra físicamente el artículo perteneciente al Usuario A y desvincula sus comentarios y etiquetas.

#### 📸 Evidencias Técnicas
* **Evidencia Automatizada (pytest):**
```text
FAILED tests/test_articles.py::test_eliminar_articulo_ajeno_retorna_400 - AssertionError: [CP-ART-A-006] Se esperaba HTTP 400, se obtuvo 200. ALERTA DE SEGURIDAD (BUG-04): la verificación de autoría en DELETE fue eliminada.
```
* **Evidencia Manual (Swagger UI):**
Captura de pantalla: [docs_qa/evidencias/CP-QUAL-M-004_delete_ajeno_bug04.png](evidencias/CP-QUAL-M-004_delete_ajeno_bug04.png)  
*(El usuario Carlos ejecuta DELETE sobre el artículo de Laura recibiendo 200 OK y eliminándolo definitivamente)*.

![Evidencia BUG-04](evidencias/CP-QUAL-M-004_delete_ajeno_bug04.png)

#### 🛡️ Criterios de Cierre y Verificación
- [ ] Incluir la guarda `if article.author_id != current_user.id: raise HTTPException(400, ...)` en `delete_article_by_slug`.
- [ ] Ejecución exitosa de `pytest tests/test_articles.py::test_eliminar_articulo_ajeno_retorna_400` (`PASSED`).
- [ ] Certificación de no-regresión en Swagger UI con cuentas separadas.

---

### Issue #5: [BUG-05] Inversión de lógica booleana en sistema de favoritos detona excepción HTTP 500 (ValueError)

#### 📋 Metadatos del Defecto
* **Identificador:** `BUG-05`
* **Módulo Afectado:** `Favorites` (Lógica de Interacción Social)
* **Caso(s) de Prueba Asociado(s):** [CP-FAV-A-001](Casos_De_Prueba.md#cp-fav-a-001), [CP-FAV-A-002](Casos_De_Prueba.md#cp-fav-a-002) *(pytest)*, [CP-EST-M-002](Casos_De_Prueba.md#cp-est-m-002) *(Swagger UI)*
* **Severidad Técnica:** `Alta`
* **Prioridad de Negocio:** `Media`
* **Estado en GitHub:** `[x] Abierto (Open)`
* **Etiquetas (Labels):** `bug`, `module: favorites`, `severity: high`, `priority: medium`, `status: open`
* **Reportado por:** Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas
* **Fecha de Reporte:** 09/11/2026
* **Asignado a:** Niurka Liseth Mejía Vargas (Issue Tracking) / Dev Team

#### 🧬 Cadena Causal ISTQB
* **Error Humano:** El programador invirtió el valor del flag booleano al invocar la capa de persistencia en el endpoint de favoritos.
* **Defecto en Código (Causa Raíz):** En `app/api/routes/articles/articles.py`, endpoint `favorite_article`, se pasa `favorite=False` a la función `change_article_favorite_state` en lugar de `favorite=True`.
* **Fallo Dinámico Observable:** Al intentar marcar un artículo como favorito por primera vez, SQLAlchemy intenta ejecutar `remove()` sobre una lista que no contiene al usuario, detonando la excepción no controlada `ValueError: list.remove(x): x not in list` y respondiendo `HTTP 500 Internal Server Error`.

#### 💼 Justificación de Impacto en el Negocio
* **Impacto en el Negocio:** Afecta severamente los mecanismos de interacción y *engagement* de los lectores. Los usuarios no pueden guardar artículos en su lista personal de favoritos ni ver actualizados los contadores de aprecio, perjudicando el algoritmo de recomendación del blog.
* **Severidad:** Alta (provoca errores 500 no controlados en el servidor).
* **Prioridad:** Media (no compromete la publicación ni borra datos principales de artículos).

#### ⚙️ Precondiciones y Datos de Prueba
* Artículo existente con `favoritesCount: 0`.
* Usuario autenticado que aún no ha marcado favorito dicho artículo.

#### 🔁 Pasos para Reproducir
1. Obtener token JWT de un usuario autenticado.
2. Enviar petición HTTP POST a `http://localhost:8000/api/articles/{slug}/favorite`.
3. Cabecera `Authorization: Bearer <token>`.
4. Observar la respuesta HTTP del servidor y el traceback generado.

#### 🎯 Comportamiento Esperado vs. Obtenido
* **Resultado Esperado:** `HTTP 200 OK`. JSON con `favorited: true` y `favoritesCount: 1`.
* **Resultado Obtenido:** `HTTP 500 Internal Server Error`. El worker colapsa con `ValueError: list.remove(x): x not in list`.

#### 📸 Evidencias Técnicas
* **Evidencia Automatizada (pytest):**
```text
FAILED tests/test_favorites.py::test_marcar_favorito_incrementa_contador - ValueError: list.remove(x): x not in list
FAILED tests/test_favorites.py::test_desmarcar_favorito_decrementa_contador
```
* **Evidencia Manual (Swagger UI):**
Captura de pantalla: [docs_qa/evidencias/CP-EST-M-002_favorite_500_bug05.png](evidencias/CP-EST-M-002_favorite_500_bug05.png)  
*(Petición POST a favorite genera HTTP 500 Internal Server Error en Swagger)*.

![Evidencia BUG-05](evidencias/CP-EST-M-002_favorite_500_bug05.png)

#### 🛡️ Criterios de Cierre y Verificación
- [ ] Corregir el paso de parámetro a `favorite=True` en `favorite_article`.
- [ ] Ejecución exitosa de `pytest tests/test_favorites.py` (`2 passed`).

---

### Issue #6: [BUG-06] Estado de relación de seguimiento hardcodeado (following: false) en perfiles de usuario

#### 📋 Metadatos del Defecto
* **Identificador:** `BUG-06`
* **Módulo Afectado:** `Profiles` (Red Social y Seguimiento de Autores)
* **Caso(s) de Prueba Asociado(s):** [CP-PRF-A-001](Casos_De_Prueba.md#cp-prf-a-001), [CP-PRF-A-002](Casos_De_Prueba.md#cp-prf-a-002) *(pytest)*, [CP-EST-M-001](Casos_De_Prueba.md#cp-est-m-001) *(Swagger UI)*
* **Severidad Técnica:** `Media`
* **Prioridad de Negocio:** `Media`
* **Estado en GitHub:** `[x] Abierto (Open)`
* **Etiquetas (Labels):** `bug`, `module: profiles`, `severity: medium`, `priority: medium`, `status: open`
* **Reportado por:** Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas
* **Fecha de Reporte:** 09/11/2026
* **Asignado a:** Niurka Liseth Mejía Vargas (Issue Tracking) / Dev Team

#### 🧬 Cadena Causal ISTQB
* **Error Humano:** El desarrollador dejó fijado un valor constante booleano (`False`) durante la construcción del objeto de transferencia de datos (DTO).
* **Defecto en Código (Causa Raíz):** En `app/models/domain/users.py`, método `profile()`, el constructor retorna siempre `Profile(..., following=False)` en lugar de evaluar si el usuario consultante figura en la relación `followers` del usuario objetivo.
* **Fallo Dinámico Observable:** Aunque la tabla intermedia `follower_user` persiste la relación correctamente en PostgreSQL, la API siempre serializa `"following": false` en la respuesta JSON.

#### 💼 Justificación de Impacto en el Negocio
* **Impacto en el Negocio:** Genera confusión en la interfaz de usuario: el botón "Seguir" permanece visualmente en estado inactivo tras presionarlo, induciendo al usuario a repetir la acción o desconfiar del funcionamiento de la red.
* **Severidad:** Media (inconsistencia lógica de serialización; la BD no se corrompe).
* **Prioridad:** Media (afecta la experiencia interactiva, pero no inutiliza la API).

#### ⚙️ Precondiciones y Datos de Prueba
* Usuario A (seguidor) autenticado con token JWT.
* Usuario B (autor a seguir) registrado en el sistema.

#### 🔁 Pasos para Reproducir
1. Enviar petición HTTP POST a `http://localhost:8000/api/profiles/{username_b}/follow`.
2. Header `Authorization: Bearer <token_usuario_a>`.
3. Inspeccionar el campo `profile.following` en el cuerpo de la respuesta.
4. Enviar un GET subsecuente a `http://localhost:8000/api/profiles/{username_b}`.

#### 🎯 Comportamiento Esperado vs. Obtenido
* **Resultado Esperado:** `HTTP 200 OK` con `"following": true`.
* **Resultado Obtenido:** `HTTP 200 OK` pero con `"following": false`.

#### 📸 Evidencias Técnicas
* **Evidencia Automatizada (pytest):**
```text
FAILED tests/test_profiles.py::test_seguir_usuario_cambia_following_a_true - AssertionError: [CP-PRF-A-001] Se esperaba following=true después de seguir, se obtuvo False.
```
* **Evidencia Manual (Swagger UI):**
Captura de pantalla: [docs_qa/evidencias/CP-EST-M-001_follow_false_bug06.png](evidencias/CP-EST-M-001_follow_false_bug06.png)  
*(POST /follow responde con following: false a pesar del registro exitoso en BD)*.

![Evidencia BUG-06](evidencias/CP-EST-M-001_follow_false_bug06.png)

#### 🛡️ Criterios de Cierre y Verificación
- [ ] Conectar la verificación dinámica de pertenencia `self.followers.filter(...)` en `User.profile()`.
- [ ] Ejecución exitosa de `pytest tests/test_profiles.py` (`2 passed`).

---

### Issue #7: [BUG-07] Endpoint de Feed personal (/api/articles/feed) accesible sin autenticación y colapsa con HTTP 500

#### 📋 Metadatos del Defecto
* **Identificador:** `BUG-07`
* **Módulo Afectado:** `Articles` (Feed y Autenticación Obligatoria)
* **Caso(s) de Prueba Asociado(s):** [CP-ART-A-007](Casos_De_Prueba.md#cp-art-a-007) *(pytest)*
* **Severidad Técnica:** `Alta`
* **Prioridad de Negocio:** `Alta`
* **Estado en GitHub:** `[x] Abierto (Open)`
* **Etiquetas (Labels):** `bug`, `security`, `module: articles`, `severity: high`, `priority: high`, `status: open`
* **Reportado por:** Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas
* **Fecha de Reporte:** 09/11/2026
* **Asignado a:** Niurka Liseth Mejía Vargas (Issue Tracking) / Dev Team

#### 🧬 Cadena Causal ISTQB
* **Error Humano:** El desarrollador configuró una inyección de dependencia permisiva (`OptionalCurrentUser`) en un endpoint cuya naturaleza de negocio requiere estrictamente conocer al usuario solicitante.
* **Defecto en Código (Causa Raíz):** En `app/api/routes/articles/articles.py`, definición de la ruta `get_user_feed`:
  ```python
  current_user: Optional[User] = Depends(get_current_user_optional) # Defecto
  ```
* **Fallo Dinámico Observable:** Al recibir una petición anónima sin cabecera de autorización, el endpoint no rechaza la petición con `HTTP 401 Unauthorized`. Al continuar la ejecución, intenta acceder a `current_user.id`, arrojando un error interno `AttributeError: 'NoneType' object has no attribute 'id'` y respondiendo `HTTP 500`.

#### 💼 Justificación de Impacto en el Negocio
* **Impacto en el Negocio:** El Feed de noticias personalizadas es la vista principal del usuario registrado. Permitir que clientes anónimos invoquen el feed y provocar caídas con errores 500 expone trazas internas del servidor, degradando la seguridad y la fiabilidad percibida de la infraestructura.
* **Severidad:** Alta (desencadena crash 500 por puntero nulo / NoneType).
* **Prioridad:** Alta (viola el contrato fundamental de autenticación de la API).

#### ⚙️ Precondiciones y Datos de Prueba
* Petición HTTP GET enviada directamente sin token de autorización Bearer.

#### 🔁 Pasos para Reproducir
1. Enviar una petición HTTP GET a `http://localhost:8000/api/articles/feed`.
2. Omitir deliberadamente la cabecera `Authorization`.
3. Observar el código de respuesta devuelto por FastAPI.

#### 🎯 Comportamiento Esperado vs. Obtenido
* **Resultado Esperado:** `HTTP 401 Unauthorized` con mensaje indicando requerimiento de credenciales de autenticación.
* **Resultado Obtenido:** `HTTP 500 Internal Server Error` debido a la desreferencia no controlada de `NoneType`.

#### 📸 Evidencias Técnicas
* **Evidencia Automatizada (pytest):**
```text
FAILED tests/test_articles.py::test_feed_sin_auth_retorna_401 - AttributeError: 'NoneType' object has no attribute 'id'
```
* **Reporte HTML:** [docs_qa/reports/test_report.html](reports/test_report.html)

#### 🛡️ Criterios de Cierre y Verificación
- [ ] Restablecer la dependencia estricta `current_user: User = Depends(get_current_user_authorizer)` en el endpoint de feed.
- [ ] Ejecución exitosa de `pytest tests/test_articles.py::test_feed_sin_auth_retorna_401` (`PASSED`).

---

### Issue #8: [BUG-08] Filtro por etiqueta (?tag=...) en GET /api/articles es ignorado devolviendo el catálogo sin filtrar

#### 📋 Metadatos del Defecto
* **Identificador:** `BUG-08`
* **Módulo Afectado:** `Articles` (Consultas y Filtros SQL)
* **Caso(s) de Prueba Asociado(s):** [CP-ART-A-008](Casos_De_Prueba.md#cp-art-a-008) *(pytest)*
* **Severidad Técnica:** `Media`
* **Prioridad de Negocio:** `Media`
* **Estado en GitHub:** `[x] Abierto (Open)`
* **Etiquetas (Labels):** `bug`, `module: articles`, `severity: medium`, `priority: medium`, `status: open`
* **Reportado por:** Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas
* **Fecha de Reporte:** 09/11/2026
* **Asignado a:** Niurka Liseth Mejía Vargas (Issue Tracking) / Dev Team

#### 🧬 Cadena Causal ISTQB
* **Error Humano:** El desarrollador comentó o removió el bloque condicional encargado de aplicar el filtro de etiquetas en el generador de consultas SQLAlchemy.
* **Defecto en Código (Causa Raíz):** En `app/crud/crud_article.py`, método `get_articles`, la sentencia condicional `if tag: query = query.filter(Article.tags.any(Tag.tag == tag))` fue excluida.
* **Fallo Dinámico Observable:** Al enviar `GET /api/articles?tag=python`, la API ignora el query param y retorna todos los registros de la base de datos (incluso artículos que solo tienen la etiqueta `java`), reportando un `articlesCount` inconsistente.

#### 💼 Justificación de Impacto en el Negocio
* **Impacto en el Negocio:** En un blog con miles de artículos, las etiquetas constituyen el mecanismo primario de navegación temática y descubrimiento. Si los filtros fallan, los lectores no encuentran los artículos de su interés y reciben información irrelevante, dañando la retención de usuarios.
* **Severidad:** Media (falla de precisión en consultas de solo lectura).
* **Prioridad:** Media (requiere corrección rápida pero no bloquea la escritura).

#### ⚙️ Precondiciones y Datos de Prueba
* Base de datos con al menos 2 artículos con etiqueta `python` y 1 artículo con únicamente etiqueta `java`.

#### 🔁 Pasos para Reproducir
1. Enviar una petición HTTP GET a `http://localhost:8000/api/articles?tag=python`.
2. Analizar el arreglo `articles` y el entero `articlesCount` de la respuesta JSON.

#### 🎯 Comportamiento Esperado vs. Obtenido
* **Resultado Esperado:** `HTTP 200 OK`. `articlesCount: 2`. La lista solo debe contener los artículos asociados al tag `python`.
* **Resultado Obtenido:** `HTTP 200 OK`. `articlesCount: 3`. Se devuelven todos los artículos de la BD, omitiendo el filtrado.

#### 📸 Evidencias Técnicas
* **Evidencia Automatizada (pytest):**
```text
FAILED tests/test_articles.py::test_filtrar_articulos_por_tag - AssertionError: [CP-ART-A-008] Se esperaban 2 artículos con tag 'python', se obtuvieron 3.
```
* **Reporte HTML:** [docs_qa/reports/test_report.html](reports/test_report.html)

#### 🛡️ Criterios de Cierre y Verificación
- [ ] Restaurar la cláusula condicional de filtrado por tag en `crud_article.py`.
- [ ] Ejecución exitosa de `pytest tests/test_articles.py::test_filtrar_articulos_por_tag` (`PASSED`).

---

### Issue #9: [BUG-09] Parámetro de paginación ?limit=100 excede el tope de 20 artículos (Falla BVA)

#### 📋 Metadatos del Defecto
* **Identificador:** `BUG-09`
* **Módulo Afectado:** `Articles` (Paginación y Rendimiento)
* **Caso(s) de Prueba Asociado(s):** [CP-ART-A-009](Casos_De_Prueba.md#cp-art-a-009) *(pytest)*, [CP-EXP-M-004](Casos_De_Prueba.md#cp-exp-m-004) *(Postman / Swagger UI)*
* **Severidad Técnica:** `Media`
* **Prioridad de Negocio:** `Media`
* **Estado en GitHub:** `[x] Abierto (Open)`
* **Etiquetas (Labels):** `bug`, `performance`, `module: articles`, `severity: medium`, `priority: medium`, `status: open`
* **Reportado por:** Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas
* **Fecha de Reporte:** 09/11/2026
* **Asignado a:** Niurka Liseth Mejía Vargas (Issue Tracking) / Dev Team

#### 🧬 Cadena Causal ISTQB
* **Error Humano:** El desarrollador suprimió la sanitización y restricción de frontera de los parámetros numéricos de paginación solicitados por el cliente.
* **Defecto en Código (Causa Raíz):** En `app/api/routes/articles/articles.py`, endpoint `get_articles`, se eliminó la instrucción de acotamiento `limit = min(limit, 20)`, transfiriendo el entero crudo provisto en la query string a la sentencia `LIMIT` de SQL.
* **Fallo Dinámico Observable:** Al solicitar `GET /api/articles?limit=100`, la API retorna 25 artículos en una sola carga en lugar de capear la entrega al umbral máximo permitido de 20 estipulado por las reglas de frontera (BVA).

#### 💼 Justificación de Impacto en el Negocio
* **Impacto en el Negocio:** Expone la infraestructura de la API a riesgos de denegación de servicio (DoS) o agotamiento de memoria en el servidor y latencias elevadas si clientes no cooperativos solicitan límites masivos (ej. `limit=10000`), sobrecargando la red y la base de datos.
* **Severidad:** Media (vulnerabilidad de rendimiento y consumo de recursos).
* **Prioridad:** Media (requiere restablecer la cota superior defensiva).

#### ⚙️ Precondiciones y Datos de Prueba
* Base de datos poblada con al menos 25 artículos registrados.

#### 🔁 Pasos para Reproducir
1. Enviar una petición HTTP GET a `http://localhost:8000/api/articles?limit=100`.
2. Contar el número de elementos contenidos en el arreglo `articles` de la respuesta JSON.

#### 🎯 Comportamiento Esperado vs. Obtenido
* **Resultado Esperado:** `HTTP 200 OK`. Longitud del arreglo `articles` $\le$ 20 artículos (el valor se capea a la frontera máxima de 20).
* **Resultado Obtenido:** `HTTP 200 OK`. Longitud del arreglo `articles` = 25 artículos (la API entrega todos los artículos solicitados sin truncamiento).

#### 📸 Evidencias Técnicas
* **Evidencia Automatizada (pytest):**
```text
FAILED tests/test_articles.py::test_limit_capeado_en_20_articulos - AssertionError: [CP-ART-A-009] Se esperaban máximo 20 artículos, se obtuvieron 25.
```
* **Evidencia Manual (Swagger UI / Postman):**
Captura de pantalla: [docs_qa/evidencias/CP-EXP-M-004_limit_100_bug09.png..png](evidencias/CP-EXP-M-004_limit_100_bug09.png..png)  
*(Petición con limit=100 devuelve 25 elementos en la lista)*.

![Evidencia BUG-09](evidencias/CP-EXP-M-004_limit_100_bug09.png..png)

#### 🛡️ Criterios de Cierre y Verificación
- [ ] Aplicar la guarda de acotamiento defensivo `limit = min(limit, 20)` en `get_articles`.
- [ ] Ejecución exitosa de `pytest tests/test_articles.py::test_limit_capeado_en_20_articulos` (`PASSED`).

---

## 🏁 4. Conclusiones y Estado del Ciclo de Vida de Defectos

1. **Eficacia Detectora:** La suite de pruebas dinámicas alcanzó un **100% de eficacia detectora de defectos (DRE)**, descubriendo los 9 bugs inyectados en la rama `buggy-version`.
2. **Condición de Salida (Exit Criteria):** El criterio normativo estipula **0 defectos críticos abiertos**. Dado que el **Issue #4 (BUG-04: Borrado de artículos ajenos - BOLA)** permanece con severidad `Crítica` y estado `Abierto`, el dictamen formal del equipo QA es **NO-GO (Bloqueo de Pase a Producción)** hasta su resolución verificada.
3. **Flujo de Trabajo en GitHub:** Cada Issue ha quedado documentado y listo para ser gestionado en el tablero Kanban de GitHub Projects / GitHub Issues del repositorio, con trazabilidad completa hacia los scripts de pytest y evidencias manuales adjuntas.


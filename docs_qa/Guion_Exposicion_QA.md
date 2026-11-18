# GUIÓN MAESTRO DE EXPOSICIÓN Y SUSTENTACIÓN ORAL
## Proyecto: Aseguramiento de Calidad (QA) — Conduit REST API (FastAPI)

> ### 📌 ESTRUCTURA GENERAL DE LA PRESENTACIÓN (FLUJO HÍBRIDO EN 2 PARTES)
> * **Equipo Expositor:** Juan Pablo Velásquez Ramírez & Niurka Liseth Mejía Vargas
> * **Docente Evaluadora:** Yury Montoya Pérez
> * **Duración Estimada:** 12 a 14 minutos
> * **Dinámica de Exposición:**
>   1. **PARTE 1 — APOYO EN DIAPOSITIVAS (Slides 1 a 8 | ~7 min):** Contexto del SUT y stack, el modelo de negocio y su jerarquía de 4 niveles de riesgo, principios ISTQB con mayor incidencia, las 5 fases del STLC, nomenclatura estándar, resumen de los 41 casos y las 4 técnicas dinámicas aplicadas.
>   2. **PARTE 2 — DEMOSTRACIÓN EN VIVO EN EL DASHBOARD (`dashboard_qa_modern.html` | ~6.5 min):** Métricas de ejecución, efectividad DRE, cobertura de caja blanca, agrupamiento de defectos, inspección en vivo de los 9 bugs (GitHub Issues y capturas de evidencia), catálogo interactivo de casos y sustentación del **Dictamen NO-GO**.

---

## ⏱️ MAPA RÁPIDO DE TIEMPOS Y REPARTO DE VOZ

| Bloque | Soporte Visual | Tema Central | Expositor Sugerido | Tiempo |
|---|---|---|---|---|
| **Diapositiva 1** | Slide 1 | Portada, Introducción a Conduit API y Stack Tecnológico | **Niurka Mejía** | `00:00 - 01:00` |
| **Diapositiva 2** | Slide 2 | El Negocio y los 4 Niveles de Jerarquía de Riesgo | **Niurka Mejía** | `01:00 - 02:30` |
| **Diapositiva 3** | Slide 3 | Principios del Testing (ISTQB) con Mayor Incidencia | **Juan Pablo Velásquez** | `02:30 - 03:30` |
| **Diapositiva 4** | Slide 4 | Aplicación de las 5 Fases del Ciclo STLC | **Niurka Mejía** | `03:30 - 04:30` |
| **Diapositiva 5** | Slide 5 | Estándar de Nomenclatura de los Casos de Prueba | **Juan Pablo Velásquez** | `04:30 - 05:15` |
| **Diapositiva 6** | Slide 6 | Resumen del Catálogo: 41 Casos (26 Auto + 15 Manuales) | **Juan Pablo Velásquez** | `05:15 - 06:00` |
| **Diapositiva 7** | Slide 7 | Técnicas de Diseño Aplicadas (EP, BVA, Estados, BOLA) | **Juan Pablo Velásquez** | `06:00 - 07:15` |
| **Diapositiva 8** | Slide 8 | Puente de Transición hacia el Dashboard Interactivo | **Ambos** | `07:15 - 07:30` |
| **Dashboard V1** | Pestaña 1 | KPIs, Fórmula de Ejecución, Clustering y Matriz Severidad/Prioridad | **Juan Pablo Velásquez** | `07:30 - 09:30` |
| **Dashboard V2** | Pestaña 2 | Ciclo de Vida de las Métricas (6 Pasos) y Fórmulas Matemáticas | **Niurka Mejía** | `09:30 - 10:30` |
| **Dashboard V3** | Pestaña 3 | Cobertura de Código por Capa (`82.78%` / `92.17%`) y Suite `pytest` | **Juan Pablo Velásquez** | `10:30 - 11:45` |
| **Dashboard V4** | Pestaña 4 | GitHub Issues (9 Bugs), Evidencia Visual de `BUG-04` y Cierre **NO-GO** | **Niurka & Juan Pablo** | `11:45 - 14:00` |

---

# PARTE 1: EXPOSICIÓN CON DIAPOSITIVAS (FUNDAMENTOS, NEGOCIO Y DISEÑO)

<div class="slide-card">
  <div class="slide-header">
    <div class="header-left">
      <span class="slide-badge">DIAPOSITIVA 1</span>
      <span class="slide-title">Portada, Introducción a Conduit API y Stack Tecnológico</span>
    </div>
    <span class="slide-meta">⏱️ 00:00 - 01:00 · 🎙️ Expone: Niurka Mejía</span>
  </div>
  <div class="slide-body">
    <p><strong>🖥️ Qué muestras en pantalla:</strong> Portada del proyecto con el nombre de la aplicación (Conduit — RealWorld Spec) y los bloques del stack tecnológico.</p>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "Buenas tardes, profesora Yury y compañeros. Hoy Juan Pablo y yo les presentaremos el proceso completo de Aseguramiento de Calidad que ejecutamos sobre <strong>Conduit API</strong>.<br><br>
      Para este taller decidimos ir más allá de una aplicación académica básica y elegimos la implementación oficial de la especificación <strong>RealWorld</strong> construida en <strong>FastAPI con Python 3.14 y PostgreSQL sobre Docker</strong>. Es un backend REST puro de 19 endpoints que funciona como el motor de una plataforma de blogs tipo <em>Medium</em>.<br><br>
      Para auditarlo a profundidad, combinamos un stack de pruebas profesional: <strong>pytest, HTTPX y pytest-cov</strong> para pruebas automatizadas de integración y cobertura, junto con <strong>Swagger UI y Postman</strong> para pruebas manuales, llevando el control de incidencias en <strong>GitHub Issues</strong>."
    </blockquote>
  </div>
</div>

<div class="slide-card">
  <div class="slide-header">
    <div class="header-left">
      <span class="slide-badge">DIAPOSITIVA 2</span>
      <span class="slide-title">La Importancia del Negocio al Plantear las Pruebas (Los 4 Niveles)</span>
    </div>
    <span class="slide-meta">⏱️ 01:00 - 02:30 · 🎙️ Expone: Niurka Mejía</span>
  </div>
  <div class="slide-body">
    <p><strong>🖥️ Qué muestras en pantalla:</strong> La pirámide/escalera visual con los 4 Niveles de Jerarquía de Riesgo del Negocio (conservando sus títulos exactos).</p>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "Un pilar que aprendimos en clase es que <strong>el testing jamás se hace al aire o al vacío</strong>; el contexto del negocio define casi en su totalidad la naturaleza de las pruebas, su severidad y su prioridad.<br><br>
      Conduit no es una calculadora ni una pasarela bancaria; es una <strong>plataforma editorial y red social</strong>. Aquí el valor primordial es la <strong>confianza del autor, la integridad de las publicaciones y la fidelización del lector</strong>. Por eso estructuramos esta jerarquía de riesgo en 4 niveles que guió todo nuestro trabajo:
      <ul>
        <li><strong>Nivel 1: Autenticación y Autoría (Vital / Crítico):</strong> La propiedad intelectual es nuestro activo más valioso. Si un usuario puede usurpar la autoría, editar publicaciones ajenas o borrar artículos de otro autor, la plataforma pierde inmediatamente a sus creadores. Por eso, cualquier falla de autorización (BOLA) tiene <em>Severidad Crítica y Prioridad Inmediata</em>.</li>
        <li><strong>Nivel 2: Integridad Editorial y Navegabilidad (Alto):</strong> Un artículo no puede publicarse sin título ni contenido; los artículos vacíos corrompen los feeds de noticias, los algoritmos de recomendación y el posicionamiento SEO.</li>
        <li><strong>Nivel 3: Engagement Social (Medio):</strong> Los botones de 'Favorito' y 'Seguir autor' retienen al lector. Si fallan, causan frustración visual, aunque los artículos siguen siendo legibles.</li>
        <li><strong>Nivel 4: Taxonomía y Metadatos (Bajo):</strong> Las etiquetas o <em>tags</em> ayudan a categorizar. Si un filtro falla, es una molestia menor que no detiene la lectura ni destruye datos patrimoniales."</li>
      </ul>
    </blockquote>
  </div>
</div>

<div class="slide-card">
  <div class="slide-header">
    <div class="header-left">
      <span class="slide-badge">DIAPOSITIVA 3</span>
      <span class="slide-title">Principios del Testing (ISTQB) con Mayor Incidencia</span>
    </div>
    <span class="slide-meta">⏱️ 02:30 - 03:30 · 🎙️ Expone: Juan Pablo Velásquez</span>
  </div>
  <div class="slide-body">
    <p><strong>🖥️ Qué muestras en pantalla:</strong> Las 3 tarjetas de principios ISTQB destacados.</p>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "Gracias, Niurka. Aunque los 7 principios de ISTQB son obligatorios y transversales, hubo <strong>tres principios</strong> que tuvieron una incidencia directa en nuestras decisiones técnicas:<br><br>
      Primero, <strong>Las pruebas dependen del contexto:</strong> Como explicó Niurka, no se prueba igual una API editorial de blogs que un software de aviónica; adaptamos nuestras validaciones al dominio de publicaciones y permisos de autor.<br><br>
      Segundo, <strong>Las pruebas exhaustivas no son posibles:</strong> No podíamos probar infinitas combinaciones de textos y números en las peticiones JSON, por lo que aplicamos <em>Partición de Equivalencia</em> y <em>Análisis de Valores Límite</em> para reducir la cantidad de entradas maximizando la detección.<br><br>
      Y tercero, el <strong>Agrupamiento de defectos (Defect Clustering):</strong> La teoría dice que la mayoría de los fallos se concentran en pocos módulos críticos. En nuestro proyecto se cumplió al pie de la letra: el <strong>66.7% de los bugs (6 de los 9)</strong> se concentraron en el módulo <code>Articles</code>."
    </blockquote>
  </div>
</div>

<div class="slide-card">
  <div class="slide-header">
    <div class="header-left">
      <span class="slide-badge">DIAPOSITIVA 4</span>
      <span class="slide-title">STLC y Cómo se Aplicó Cada Fase en el Proyecto</span>
    </div>
    <span class="slide-meta">⏱️ 03:30 - 04:30 · 🎙️ Expone: Niurka Mejía</span>
  </div>
  <div class="slide-body">
    <p><strong>🖥️ Qué muestras en pantalla:</strong> El flujo horizontal de las 5 fases del STLC.</p>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "Para garantizar orden metodológico, recorrimos rigurosamente las 5 fases del <strong>Ciclo de Vida de las Pruebas (STLC)</strong>:
      <ol>
        <li>En <strong>Test Analysis (Análisis)</strong> respondimos al <em>¿Qué probar?</em>, auditando los 19 endpoints de la especificación RealWorld e identificando las condiciones de prueba.</li>
        <li>En <strong>Test Design (Diseño)</strong> definimos el <em>¿Cómo probar?</em>, especificando formalmente los casos de prueba, sus precondiciones y los datos de entrada.</li>
        <li>En <strong>Test Implementation (Implementación)</strong> dejamos todo listo: levantamos PostgreSQL en Docker, construimos los scripts automatizados en <code>pytest</code> y preparamos las colecciones en Postman y Swagger.</li>
        <li>En <strong>Test Execution (Ejecución)</strong> contrastamos el resultado real contra el esperado sobre dos ramas: la rama limpia <code>main</code> y la rama de evaluación <code>buggy-version</code>, capturando evidencias y reportando los defectos en GitHub Issues.</li>
        <li>Y en <strong>Test Completion (Cierre)</strong> evaluamos los criterios de salida, consolidamos las métricas en el Dashboard y redactamos el Informe de Análisis de Calidad."</li>
      </ol>
    </blockquote>
  </div>
</div>

<div class="slide-card">
  <div class="slide-header">
    <div class="header-left">
      <span class="slide-badge">DIAPOSITIVA 5</span>
      <span class="slide-title">Nomenclatura Estándar de Casos de Prueba</span>
    </div>
    <span class="slide-meta">⏱️ 04:30 - 05:15 · 🎙️ Expone: Juan Pablo Velásquez</span>
  </div>
  <div class="slide-body">
    <p><strong>🖥️ Qué muestras en pantalla:</strong> Esquema visual <code>CP - [MÓDULO] - [MODO] - [NÚMERO]</code> con la lista de módulos y modos.</p>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "Para mantener una trazabilidad bidireccional impecable entre los requisitos, las pruebas y los defectos en GitHub Issues, diseñamos este estándar de nomenclatura:<br><br>
      Cada identificador inicia con el prefijo <code>CP</code>, seguido del código del <strong>Módulo</strong> evaluado —por ejemplo <code>AUTH</code> para autenticación, <code>ART</code> para artículos, <code>QUAL</code> para atributos de calidad y seguridad, o <code>EST</code> para transición de estados—.<br><br>
      Luego indicamos el <strong>Modo de ejecución</strong>: la letra <code>A</code> cuando es un caso automatizado en <code>pytest</code> (como <code>CP-AUTH-A-001</code>) y la letra <code>M</code> cuando es un caso manual ejecutado en Swagger UI o Postman (como <code>CP-QUAL-M-004</code>), cerrando con el consecutivo numérico."
    </blockquote>
  </div>
</div>

<div class="slide-card">
  <div class="slide-header">
    <div class="header-left">
      <span class="slide-badge">DIAPOSITIVA 6</span>
      <span class="slide-title">Resumen del Catálogo: 41 Casos de Prueba Diseñados y Ejecutados</span>
    </div>
    <span class="slide-meta">⏱️ 05:15 - 06:00 · 🎙️ Expone: Juan Pablo Velásquez</span>
  </div>
  <div class="slide-body">
    <p><strong>🖥️ Qué muestras en pantalla:</strong> Tabla consolidada de los 41 casos de prueba (26 automatizados + 15 manuales).</p>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "Con esta estructura superamos la meta mínima del taller de 40 casos, diseñando y ejecutando un total de <strong>41 casos de prueba</strong> que cubren el <strong>100% de los 19 endpoints</strong> de la API:<br><br>
      Construimos una base sólida de <strong>26 casos automatizados (el 63.4%)</strong> usando <code>pytest</code>, <code>pytest-asyncio</code> y <code>HTTPX</code>, distribuidos en todos los módulos funcionales para asegurar regresión inmediata.<br><br>
      Y la complementamos con <strong>15 casos manuales (el 36.6%)</strong> en Swagger UI y Postman, enfocados en pruebas exploratorias, validación de herramientas, seguridad multi-usuario y transiciones de estado donde la inspección visual humana aporta mayor valor."
    </blockquote>
  </div>
</div>

<div class="slide-card">
  <div class="slide-header">
    <div class="header-left">
      <span class="slide-badge">DIAPOSITIVA 7</span>
      <span class="slide-title">Técnicas de Diseño de Pruebas Dinámicas Aplicadas</span>
    </div>
    <span class="slide-meta">⏱️ 06:00 - 07:15 · 🎙️ Expone: Juan Pablo Velásquez</span>
  </div>
  <div class="slide-body">
    <p><strong>🖥️ Qué muestras en pantalla:</strong> Cuadrícula 2x2 con las 4 técnicas aplicadas y sus ejemplos reales.</p>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "En el diseño de estos 41 casos aplicamos cuatro técnicas dinámicas concretas:
      <ol>
        <li><strong>Partición de Equivalencia (EP):</strong> Dividimos las entradas en particiones válidas (que deben responder 200 o 201) e inválidas (que deben rechazarse con 400 o 422), como el registro con email válido frente a emails duplicados o sin formato arroba, y títulos vacíos.</li>
        <li><strong>Análisis de Valores Límite (BVA):</strong> Evaluamos las fronteras del dominio. En los casos <code>CP-ART-A-009</code> y <code>CP-EXP-M-004</code> probamos la regla de paginación cuyo tope máximo es de 20 artículos por página; enviamos <code>?limit=100</code> con 25 artículos en base de datos y descubrimos el <strong>BUG-09</strong>, pues la API devolvió los 25 sin truncar.</li>
        <li><strong>Transición de Estados:</strong> Evaluamos los ciclos dinámicos de <em>No seguido → Seguir → Dejar de seguir</em> y <em>Marcar favorito → Desmarcar favorito</em>, lo que nos permitió capturar los defectos <strong>BUG-05</strong> y <strong>BUG-06</strong>.</li>
        <li><strong>Pruebas de Seguridad y Control de Acceso (BOLA / IDOR):</strong> Simulamos vectores de ataque donde un usuario autenticado intenta editar o eliminar artículos creados por otro autor, destapando las brechas más graves del sistema: <strong>BUG-03</strong> y <strong>BUG-04</strong>."</li>
      </ol>
    </blockquote>
  </div>
</div>

<div class="slide-card">
  <div class="slide-header">
    <div class="header-left">
      <span class="slide-badge">DIAPOSITIVA 8</span>
      <span class="slide-title">Transición al Dashboard en Vivo</span>
    </div>
    <span class="slide-meta">⏱️ 07:15 - 07:30 · 🎙️ Exponen: Ambos</span>
  </div>
  <div class="slide-body">
    <p><strong>🖥️ Acción en vivo:</strong> Mostrar brevemente la Diapositiva 8 y hacer <code>Alt + Tab</code> hacia el navegador con <code>dashboard_qa_modern.html</code> abierto en la Pestaña 1.</p>
    <p><strong>🗣️ Frase de puente (Juan Pablo):</strong></p>
    <blockquote>
      "Habiendo establecido cómo planificamos y diseñamos las pruebas desde el negocio, pasemos ahora a nuestro <strong>Tablero Ejecutivo de Métricas QA en vivo</strong> para analizar los resultados obtenidos, las evidencias de los 9 defectos y la decisión final de lanzamiento."
    </blockquote>
  </div>
</div>

---

# PARTE 2: RECORRIDO EN VIVO EN EL DASHBOARD (`dashboard_qa_modern.html`)

> ### 💡 INSTRUCCIÓN PRÁCTICA PARA LA DEMO EN VIVO
> A partir de este momento ya no necesitas diapositivas. Todo el resto de la exposición (Métricas, Fórmulas, Cobertura de Caja Blanca, Reportes en GitHub Issues, Evidencias Fotográficas y Análisis de Calidad) está contenido dentro de las **4 pestañas del Dashboard**.

<div class="dash-card">
  <div class="dash-header">
    <div class="header-left">
      <span class="dash-badge">PESTAÑA 1 DEL DASHBOARD</span>
      <span class="dash-title">1. Resumen y Decisión (KPIs, Ejecución, Clustering y Matriz)</span>
    </div>
    <span class="dash-meta">⏱️ 07:30 - 09:30 · 🎙️ Expone: Juan Pablo Velásquez</span>
  </div>
  <div class="dash-body">
    <p><strong>🖱️ Ruta de clics en pantalla:</strong></p>
    <ol>
      <li>Señalar las <strong>6 tarjetas KPI superiores</strong>.</li>
      <li>Señalar el gráfico Donut de <strong>Fórmula Base de Ejecución</strong> (y mostrar rápidamente en el selector superior el cambio entre <code>Ciclo 1: buggy-version</code> y <code>Ciclo 0: main</code>).</li>
      <li>Señalar el gráfico de barras rojas de <strong>Agrupamiento de Defectos (Defect Clustering)</strong> y la <strong>Matriz Cruzada de Severidad vs. Prioridad</strong>.</li>
    </ol>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "En esta primera vista ejecutiva consolidamos el estado de salud del producto:<br><br>
      Primero, en las tarjetas superiores vemos una <strong>Cobertura de Ejecución del 100%</strong> (41 de 41 casos ejecutados) y una <strong>Efectividad de Detección (DRE) del 100%</strong> (los 9 defectos presentes fueron detectados en QA antes de llegar a producción).<br><br>
      Observen la <strong>Tasa de Aprobación del 58.54%</strong> (24 casos aprobados y 17 fallidos). Aquí es vital hacer una lectura de ingeniería: que el 41.46% de los casos falle en la rama <code>buggy-version</code> <strong>no significa que la suite sea inestable</strong>; si cambiamos aquí arriba al <em>Ciclo 0: rama main limpia</em> [mostrar en el selector], el 100% de las pruebas pasan en verde. En la rama con errores, esos 17 fallos son nuestras pruebas cumpliendo su misión de cazar los 9 bugs inyectados.<br><br>
      A la derecha vemos demostrado gráficamente el principio de <strong>Defect Clustering</strong>: 6 de los 9 defectos (66.7%) están concentrados en <code>Articles</code>, mientras que módulos como <code>Comments</code> y <code>Tags</code> operan al 100% sin fallos.<br><br>
      Y aquí abajo en la <strong>Matriz Cruzada de Severidad Técnica vs. Prioridad de Negocio</strong> vemos por qué fue tan importante separar ambos conceptos: por ejemplo, el <code>BUG-05</code> tiene <em>Severidad Alta</em> porque arroja un Error 500 en favoritos, pero tiene <em>Prioridad Media</em> porque no destruye artículos; mientras que el <code>BUG-04</code> combina <em>Severidad Crítica con Prioridad Alta</em> al comprometer la seguridad de toda la plataforma."
    </blockquote>
  </div>
</div>

<div class="dash-card">
  <div class="dash-header">
    <div class="header-left">
      <span class="dash-badge">PESTAÑA 2 DEL DASHBOARD</span>
      <span class="dash-title">2. Ciclo de Métricas y Fórmulas Matemáticas</span>
    </div>
    <span class="dash-meta">⏱️ 09:30 - 10:30 · 🎙️ Expone: Niurka Mejía</span>
  </div>
  <div class="dash-body">
    <p><strong>🖱️ Ruta de clics en pantalla:</strong></p>
    <ol>
      <li>Hacer clic en la pestaña <strong><code>2. Ciclo de Métricas y Fórmulas</code></strong>.</li>
      <li>Hacer clic en un par de tarjetas de los <strong>6 Pasos Encadenados del Ciclo de Vida de las Métricas</strong> (ej. Paso 3 Validar y Paso 6 Decidir).</li>
      <li>Señalar las <strong>6 tarjetas de Fórmulas Matemáticas</strong> en la parte inferior.</li>
    </ol>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "Al pasar a la segunda pestaña, documentamos el rigor metodológico con el que construimos los indicadores siguiendo el <strong>Ciclo de Vida de las Métricas de 6 pasos</strong> visto en clase:<br><br>
      No nos limitamos a recolectar números: definimos qué queríamos medir, recolectamos los datos crudos desde los reportes JSON de <code>pytest</code> y las ejecuciones manuales, y aplicamos el paso crítico de <strong>Validación bajo el principio 'Garbage In, Garbage Out'</strong> para asegurar que no hubiera datos corruptos antes de analizarlos.<br><br>
      Aquí abajo están verificadas las <strong>6 fórmulas matemáticas</strong> con nuestros datos reales: desde la densidad de defectos de <strong>0.220 bugs por caso de prueba</strong> (equivalente a 13.5 bugs por cada mil líneas de código), hasta una tasa de fuga y reapertura del 0% en esta primera iteración."
    </blockquote>
  </div>
</div>

<div class="dash-card">
  <div class="dash-header">
    <div class="header-left">
      <span class="dash-badge">PESTAÑA 3 DEL DASHBOARD</span>
      <span class="dash-title">3. Cobertura de Código (Caja Blanca) y Suite Automatizada pytest</span>
    </div>
    <span class="dash-meta">⏱️ 10:30 - 11:45 · 🎙️ Expone: Juan Pablo Velásquez</span>
  </div>
  <div class="dash-body">
    <p><strong>🖱️ Ruta de clics en pantalla:</strong></p>
    <ol>
      <li>Hacer clic en la pestaña <strong><code>3. Cobertura y Suite pytest</code></strong>.</li>
      <li>Señalar el gráfico de <strong>Cobertura por Capa Arquitectónica</strong> y el cuadro azul de <em>Análisis de Causa Raíz (82.78% vs 92.17%)</em>.</li>
      <li>Señalar a la derecha el <strong>Verificador de Integridad JSON</strong> (puedes hacer clic en <em>"Probar Error JSON Inválido"</em> para mostrar cómo el dashboard rechaza datos corruptos) y las tablas inferiores de archivos Python y los 26 tests.</li>
    </ol>
    <p><strong>🗣️ Guion palabra por palabra:</strong></p>
    <blockquote>
      "En la tercera pestaña conectamos las pruebas de caja negra con la <strong>cobertura estructural de caja blanca</strong> medida con <code>pytest-cov</code>:<br><br>
      Alcanzamos un <strong>82.78% de cobertura global de sentencias</strong> (553 de 668 líneas ejecutadas), superando ampliamente la meta del 70%. Pero hicimos un análisis de causa raíz aún más profundo: notamos que las 68 líneas sin cubrir del archivo <code>app/seed.py</code> corresponden a un script auxiliar de consola para poblar datos de prueba iniciales que jamás se ejecuta cuando el servidor API está en producción. Si excluimos ese script CLI, la <strong>cobertura real del runtime de nuestra API es del 92.17%</strong> (con el 100% en Modelos SQLAlchemy y el 100% en Esquemas Pydantic).<br><br>
      Además, implementamos aquí a la derecha un validador de integridad en vivo que rechaza archivos JSON malformados, y aquí abajo podemos filtrar los 29 módulos de Python y los <strong>26 scripts de pytest</strong> que se ejecutan en apenas 28.92 segundos."
    </blockquote>
  </div>
</div>

<div class="dash-card">
  <div class="dash-header">
    <div class="header-left">
      <span class="dash-badge">PESTAÑA 4 + CIERRE</span>
      <span class="dash-title">4. Defectos en GitHub Issues, Evidencia de BUG-04 y Dictamen NO-GO</span>
    </div>
    <span class="dash-meta">⏱️ 11:45 - 14:00 · 🎙️ Exponen: Niurka & Juan Pablo</span>
  </div>
  <div class="dash-body">
    <p><strong>🖱️ Ruta de clics en pantalla:</strong></p>
    <ol>
      <li>Hacer clic en la pestaña <strong><code>4. Defectos (9) y Casos (41)</code></strong> y mostrar la tabla de los <strong>9 Defectos registrados en GitHub Issues</strong>.</li>
      <li><strong>¡CLIC ESTRELLA!:</strong> Hacer clic en el botón <strong><code>Ver Ficha / Captura</code> del <code>BUG-04</code></strong> para abrir el modal con la captura de Swagger UI.</li>
      <li>Cerrar el modal, mostrar el buscador de los 41 casos de prueba abajo, y finalmente subir al banner rojo superior y hacer clic en <strong><code>Autorizar Pase a Producción</code></strong> para mostrar el bloqueo de seguridad.</li>
    </ol>
    <p><strong>🗣️ Guion palabra por palabra (Niurka — Defectos y BUG-04):</strong></p>
    <blockquote>
      "Finalmente, en la cuarta pestaña tenemos la trazabilidad completa de los <strong>9 defectos reportados en GitHub Issues</strong> y el catálogo de los 41 casos de prueba.<br><br>
      Cada ficha de bug fue refinada aplicando la <strong>Cadena Causal de ISTQB</strong>: distinguimos el <em>Error Humano</em> del programador, el <em>Defecto estático en el código fuente</em> (indicando archivo y línea exacta) y el <em>Fallo dinámico observable</em>.<br><br>
      Si abrimos aquí la ficha del <strong>BUG-04</strong> [hacer clic en BUG-04], vemos por qué este hallazgo detiene el lanzamiento: en el archivo <code>articles.py</code> se omitió verificar que el usuario autenticado sea el autor del artículo antes de ejecutar un <code>DELETE</code>. Como se observa en nuestra evidencia en Swagger UI, el usuario Carlos envió una petición DELETE sobre el artículo de Laura y el servidor respondió <code>200 OK</code>, borrando permanentemente el trabajo de otro autor."
    </blockquote>
    <p><strong>🗣️ Guion palabra por palabra (Juan Pablo — Dictamen NO-GO y Cierre):</strong></p>
    <blockquote>
      "Esto nos lleva a nuestra conclusión y análisis de calidad final. Si alguien en la dirección del proyecto intenta presionar este botón de <strong>'Autorizar Pase a Producción'</strong> [hacer clic en el botón para abrir el modal de bloqueo], nuestro sistema de control lo bloquea.<br><br>
      ¿Por qué emitimos un <strong>Dictamen Formal NO-GO</strong> si ejecutamos el 100% de las pruebas y tenemos más del 82% de cobertura de código? Porque una cobertura alta jamás compensa una brecha crítica de seguridad abierta. Nuestro criterio de salida exige <strong>cero defectos críticos abiertos</strong>.<br><br>
      Para pasar a un estado <strong>GO</strong>, dejamos trazado el plan de remediación en 3 pasos: 1) Aplicar las guardas de propiedad en <code>articles.py</code> y corregir las validaciones en los esquemas; 2) Ejecutar <em>Re-testing</em> sobre los 9 fallos y correr los 26 tests automatizados de regresión en menos de 30 segundos; y 3) Cerrar los 9 issues en GitHub. Con esto demostramos cómo el aseguramiento de calidad protege la continuidad y la reputación del negocio. ¡Muchas gracias!"
    </blockquote>
  </div>
</div>

---

## 🎯 CHECKLIST DE PREPARACIÓN 5 MINUTOS ANTES DE EXPONER

<div class="slide-card" style="background:#F8FAFC;">
  <div class="slide-body">
    <ul>
      <li><strong>Ventana 1 (Diapositivas):</strong> Tus 8 diapositivas listas en pantalla completa para cubrir los fundamentos, los 4 niveles de riesgo del negocio, principios ISTQB, STLC, nomenclatura, tabla de 41 CPs y las 4 técnicas dinámicas.</li>
      <li><strong>Ventana 2 (Dashboard en Vivo):</strong> El archivo <code>docs_qa/reports/dashboard_qa_modern.html</code> (o su versión oscura <code>dashboard_qa_dark.html</code>) abierto en el navegador en la <strong>Pestaña 1</strong> con el selector en <code>Ciclo 1: buggy-version (Actual)</code>.</li>
      <li><strong>El "Momento Wow" frente a la docente:</strong> En el Dashboard, alternar el selector entre <code>Ciclo 1: buggy-version</code> (NO-GO, 58.54% Pass) y <code>Ciclo 0: main</code> (GO, 100% Pass), abrir en vivo el modal del <strong>BUG-04</strong> con la captura de Swagger UI, y pulsar el botón <strong>Autorizar Pase a Producción</strong> para demostrar el bloqueo activo del Release Gate.</li>
    </ul>
  </div>
</div>

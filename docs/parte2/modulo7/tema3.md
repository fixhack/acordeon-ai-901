# Tema 3: Qué diferencia hay técnicamente y en respuesta entre usar Foundry IQ y cargar archivos directo al agente de Microsoft Foundry

### Descripción
En Foundry hay dos formas comunes de darle documentos a un agente:
1. **Cargar archivos directo al agente** (herramienta **File Search** / *Knowledge → Files*): subes PDFs al agente y Foundry crea un **vector store** solo para él.
2. **Conectar una base de conocimiento de Foundry IQ**: una capa de conocimiento **compartida** sobre Azure AI Search, con varias fuentes y **recuperación agéntica**.

Analogía: cargar archivos al agente es como darle a un empleado una **carpeta personal** con 20 documentos. Foundry IQ es darle acceso a la **biblioteca corporativa** con bibliotecario: miles de documentos de distintas áreas, siempre actualizados, que comparten todos los empleados y que solo muestran lo que cada quien tiene permiso de ver.

### Aspectos Clave

1. **Diferencias técnicas:**

   | Aspecto | Archivos directos (File Search) | Foundry IQ |
   |---|---|---|
   | Dónde viven los datos | Vector store administrado, asociado al agente | Índices de **Azure AI Search** + fuentes remotas |
   | Fuentes | Archivos que subes manualmente | SharePoint, Blob Storage, OneLake, web, Azure SQL, índices existentes, Work IQ... |
   | Alcance | Un agente (o pocos) | **Compartido** por muchos agentes y apps |
   | Indexación | Automática al subir (chunking + embeddings) | Automática y **continua** sobre las fuentes (chunking, embeddings, metadatos) |
   | Actualización | Vuelves a subir los archivos | Se sincroniza con la fuente de verdad |
   | Tipo de búsqueda | Vectorial (+ palabras clave) sobre fragmentos | Palabras clave, vectorial o **híbrida** + ranking semántico |
   | Estrategia de recuperación | Una búsqueda por consulta | **Recuperación agéntica**: un LLM planea subconsultas, busca en paralelo en varias fuentes y fusiona resultados |
   | Permisos | Los del agente (todos ven lo mismo) | **Por usuario** en fuentes compatibles (y etiquetas de Purview) |
   | Gobernanza | Por agente | Centralizada por dominio de negocio |
   | Conexión al agente | Herramienta File Search integrada | **Herramienta MCP** (`knowledge_base_retrieve`) |
   | Costo y complejidad | Bajo; listo en minutos | Mayor: requiere Azure AI Search y configuración |

2. **Diferencias en la respuesta:**

   | Pregunta del usuario | Archivos directos | Foundry IQ |
   |---|---|---|
   | Simple, una fuente: "¿Cuántos días de vacaciones tengo?" | ✅ Responde bien | ✅ Responde bien |
   | Compuesta: "Compara la política de viáticos de 2025 con la de 2026 y dime qué cambió para viajes a Europa" | ⚠️ Una sola búsqueda puede traer solo una de las políticas | ✅ Divide en subconsultas (2025, 2026, Europa), busca cada una y combina |
   | Varias fuentes: "¿Qué dice la política y qué gastos registré el mes pasado?" | ❌ Solo ve los archivos subidos | ✅ Consulta SharePoint + base de datos |
   | Información que cambió ayer | ❌ Solo si alguien volvió a subir el archivo | ✅ Si la fuente está sincronizada |
   | Documento confidencial de Dirección | ⚠️ Lo ve cualquiera que use el agente | ✅ Solo si el usuario tiene permiso |
   | Citas | ✅ Al archivo | ✅ A la fuente original (con URL, sitio de SharePoint...) |

3. **Cuándo usar cada uno:**
   - **Archivos directos:**
     - Prototipos, demos y pruebas de concepto.
     - Pocos documentos estables (un manual, unas FAQ).
     - Un solo agente; todos los usuarios pueden ver todo.
   - **Foundry IQ:**
     - Producción empresarial con muchos documentos y varias fuentes.
     - Varios agentes que comparten conocimiento por dominio ("Finanzas", "RR. HH.").
     - Se requieren permisos por usuario, frescura y gobernanza central.
     - Preguntas complejas que se benefician de la recuperación agéntica.

4. **El costo oculto de NO usar una capa compartida:**
   Microsoft Learn pone el ejemplo de tres agentes (finanzas, instalaciones y vacaciones). Si cada uno tiene su propio RAG, se **duplican** procesamiento, embeddings, índices, lógica de recuperación, permisos y monitoreo, y los resultados pueden ser **inconsistentes** entre agentes. Con Foundry IQ, una mejora en la base de conocimiento beneficia a todos los agentes conectados.

### Para el examen
- "Prototipo rápido con un PDF" → subir el archivo al agente (File Search).
- "Conocimiento reutilizable por varios agentes, con permisos y varias fuentes empresariales" → **Foundry IQ**.
- "¿Qué proceso divide la pregunta en subconsultas y busca en varias fuentes?" → **recuperación agéntica**.

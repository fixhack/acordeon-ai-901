# Tema 2: Comprender la diferencia entre los modelos y los agentes y cuándo usar uno u otro

### Descripción
Microsoft Learn lo resume así: **los modelos son inteligencia en bruto**; **los agentes son trabajadores empaquetados y orientados a tareas** construidos sobre esa inteligencia. Un modelo responde a un prompt; un agente tiene un rol fijo, herramientas para actuar, conocimiento para fundamentarse y memoria dentro de la conversación.

Analogía: un **modelo** es un recién egresado brillante al que le preguntas cualquier cosa y te contesta con lo que sabe. Un **agente** es ese mismo egresado ya contratado: tiene un puesto (instrucciones), acceso al sistema de la empresa (herramientas), al manual interno (conocimiento) y recuerda lo que platicaron en la junta (memoria).

### Aspectos Clave

1. **Comparación (basada en Microsoft Learn):**

   | Aspecto | Modelo solo | Agente |
   |---|---|---|
   | Alcance | Prompt → respuesta, una vez | Comportamiento consistente tipo flujo de trabajo, reutilizable |
   | Componentes | Modelo (+ prompt) | Modelo + **instrucciones** + **herramientas** (+ conocimiento) |
   | Acciones | Solo genera texto | Llama herramientas: busca, lee, escribe, actualiza sistemas |
   | Contexto | Solo lo que va en el prompt | Fundamentado con conocimiento (RAG) y citas |
   | Memoria | Limitada al intercambio actual | Memoria de trabajo durante la conversación |
   | Empaquetado | Se prueba en el Playground | Componente con nombre, versionado y reutilizable |
   | Llamada en código | `responses.create(model="gpt-4.1-mini", ...)` | `responses.create(..., agent_reference=...)` |

2. **Usa un modelo directamente cuando:**
   - La tarea es **una sola transformación**: resumir, traducir, clasificar, extraer a JSON, generar un correo.
   - No necesitas herramientas ni datos privados.
   - Quieres **máximo control** y mínima latencia/costo.
   - Estás **experimentando** con prompts en el Playground.

3. **Usa un agente cuando:**
   - La tarea requiere **varios pasos** y decidir qué hacer en cada uno.
   - Necesitas **actuar** sobre otros sistemas (crear un ticket, consultar una API, enviar un correo).
   - Debe responder con **datos privados** y citarlos (knowledge / Foundry IQ).
   - Vas a **reutilizar** el mismo comportamiento en varias apps (web, Teams, bot) con instrucciones centralizadas.
   - Necesitas **gobernanza**: guardrails por agente, evaluación, trazas, versiones.

4. **Herramientas = acciones; conocimiento = contexto:**
   - **Herramientas (tools):** capacidades que el agente puede invocar: búsqueda web, consultar una base de datos, un servidor **MCP**, **Code Interpreter**, funciones o APIs (OpenAPI). Se configuran en el **Foundry Tool Catalog**.
   - **Conocimiento (knowledge):** acceso a contenido externo por RAG: PDFs internos, SharePoint, Azure Storage, bases de conocimiento de Foundry IQ. Las respuestas incluyen **citas**.

5. **Espectro de autonomía:**
   ```
   Modelo + prompt  →  Modelo + RAG  →  Agente con herramientas  →  Workflow multiagente
   (más control, más barato)                                    (más autonomía, más complejo)
   ```
   Empieza por la izquierda y avanza solo cuando el caso lo justifique.

### Mismo caso, dos enfoques
**Caso:** "¿Cuántos días de vacaciones me quedan?"
- **Con modelo:** responde algo genérico ("según la Ley Federal del Trabajo...") porque no conoce tus datos.
- **Con agente:** consulta la política (knowledge), llama a la API de RR. HH. con tu número de empleado (tool) y responde "Te quedan 6 días; vencen el 31 de diciembre [Fuente: Política de vacaciones 2026]".

```python
# Modelo directo: inteligencia en bruto
r = openai_client.responses.create(
    model="gpt-4.1-mini",
    instructions="Eres un asistente de RR. HH.",
    input="¿Cuántos días de vacaciones me quedan?",
)

# Agente: rol + herramientas + conocimiento ya configurados en Foundry
r = openai_client.responses.create(
    input="¿Cuántos días de vacaciones me quedan?",
    extra_body={"agent_reference": {"name": "agente-rrhh", "type": "agent_reference"}},
)
```
- **Explicación:** en la primera llamada **tu código** define todo en cada petición. En la segunda, el agente ya trae su configuración desde Foundry; tu cliente solo lo referencia.

### Para el examen
- "Probar rápidamente cómo responde un modelo a distintos prompts" → **Playground de modelos**.
- "Una solución que consulte documentos internos y cree tickets automáticamente" → **agente** con knowledge + tools.
- "¿Qué parte del agente define su rol?" → **instrucciones**. "¿Qué le permite actuar?" → **herramientas**.

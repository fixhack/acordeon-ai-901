# Tema 2: Introducción a los MCP (Model Context Protocol)

### Descripción
El **Model Context Protocol (MCP)** es un **estándar abierto** que define cómo los agentes de IA se conectan con herramientas y fuentes de datos externas. Fue publicado por Anthropic en noviembre de 2024 y hoy lo soportan OpenAI, Microsoft (Foundry, Copilot Studio, VS Code, Windows), Google y miles de servidores de la comunidad.

Analogía de Microsoft Learn: MCP es un **adaptador universal**, como el USB-C. Antes, cada herramienta necesitaba su propio "cable" (código de integración a la medida) para cada agente. Con MCP, cualquier agente compatible se conecta con cualquier servidor compatible.

### Aspectos Clave

1. **Arquitectura cliente-servidor:**
   ```
   ┌──────────────────────┐        MCP         ┌──────────────────────────┐
   │ Host / Cliente MCP   │ ◄────────────────► │ Servidor MCP             │
   │ (el agente: Foundry, │   descubre e       │ (expone herramientas:    │
   │  VS Code, Claude...) │   invoca tools     │  Azure Language, GitHub, │
   └──────────────────────┘                    │  tu base de datos...)    │
                                               └──────────────────────────┘
   ```
   - **Cliente MCP:** el agente (o la aplicación que lo ejecuta). Envía peticiones y recibe respuestas.
   - **Servidor MCP:** el servicio que expone capacidades. Las ejecuta y devuelve un **resultado estructurado**.
   - El agente **descubre** qué herramientas ofrece el servidor (nombre, descripción, parámetros) y decide cuándo usarlas.

2. **Lo que puede exponer un servidor MCP:**
   - **Tools (herramientas):** acciones que el modelo puede invocar (`analizar_sentimiento`, `crear_ticket`).
   - **Resources (recursos):** datos de solo lectura (archivos, registros).
   - **Prompts:** plantillas de prompt reutilizables.

3. **Transportes:**
   - **stdio:** el servidor corre como proceso local (típico en VS Code o apps de escritorio).
   - **Streamable HTTP:** el servidor corre remoto en una URL (lo que usa Foundry).

4. **¿Por qué importa?**
   - **Reutilización:** un servidor MCP sirve para muchos agentes y plataformas.
   - **Desacoplamiento:** cambias o actualizas la herramienta sin tocar el agente.
   - **Ecosistema:** GitHub, Azure, bases de datos, Microsoft Learn Docs, etc. ya tienen servidores MCP.
   - **Seguridad:** puedes exigir **aprobación** antes de que el agente ejecute una herramienta.

5. **MCP en Microsoft Foundry:**
   - **Servidor MCP de Azure Language:** servicio administrado que expone NER, sentimiento y detección de idioma. No necesitas llamar al REST de Language ni manejar tokens en el código del agente.
     1. Despliega un modelo y guárdalo como agente.
     2. En el Playground agrega una herramienta buscando *Azure Language in Foundry Tools*.
     3. Configura la conexión con el **nombre de tu recurso de Foundry**.
     4. Pide al agente que analice texto.
   - **Foundry IQ** expone cada base de conocimiento como **herramienta MCP** ([Módulo 7](../modulo7/tema4.md)).
   - Puedes conectar **cualquier servidor MCP remoto** desde el catálogo de herramientas o por código.

### Práctica: agente de Foundry con un servidor MCP (Python)
```python
# pip install "azure-ai-projects>=2.0.0" openai azure-identity python-dotenv
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

load_dotenv()
project_client = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                                 credential=DefaultAzureCredential())

# 1) Definir la herramienta MCP: servidor público de documentación de Microsoft Learn
mcp_learn = MCPTool(
    server_label="microsoft_learn",
    server_url="https://learn.microsoft.com/api/mcp",
    require_approval="never",          # "always" para exigir aprobación humana
)

# 2) Crear el agente con la herramienta
agente = project_client.agents.create_version(
    agent_name="agente-docs",
    definition=PromptAgentDefinition(
        model=os.environ["FOUNDRY_MODEL_NAME"],
        instructions="Respondes dudas de Azure en español usando SOLO la documentación de Microsoft Learn "
                     "que obtengas con tu herramienta. Incluye el enlace de la fuente.",
        tools=[mcp_learn],
    ),
)

# 3) Preguntar
openai_client = project_client.get_openai_client()
r = openai_client.responses.create(
    input="¿Qué rol necesito para crear agentes en Microsoft Foundry?",
    extra_body={"agent_reference": {"name": agente.name, "type": "agent_reference"}},
)
print(r.output_text)
```
- **Explicación:**
  - `MCPTool` registra un servidor MCP remoto. `server_label` es un nombre para identificarlo en las llamadas.
  - El agente **descubre** las herramientas del servidor (búsqueda en documentación) y decide cuándo usarlas.
  - `require_approval="always"` hace que la respuesta incluya una solicitud de aprobación (`mcp_approval_request`) que tu app debe aceptar antes de ejecutar la herramienta. Útil para acciones sensibles (borrar, pagar, enviar).

### Riesgos y buenas prácticas
- **Confía solo en servidores conocidos:** un servidor MCP malicioso puede devolver instrucciones ocultas (*prompt injection* indirecto) o exfiltrar datos.
- **Mínimo privilegio:** limita qué herramientas puede usar el agente (`allowed_tools`).
- **Aprobación humana** para acciones con efectos irreversibles.
- **Guardrails** sobre llamadas y respuestas de herramientas (intervention points *tool call* y *tool response*).

### Recursos
- [Especificación oficial de MCP](https://modelcontextprotocol.io/)
- [Servidor MCP de Microsoft Learn](https://learn.microsoft.com/es-es/training/support/mcp)
- [MCP for Beginners (curso gratuito de Microsoft en GitHub)](https://github.com/microsoft/mcp-for-beginners)

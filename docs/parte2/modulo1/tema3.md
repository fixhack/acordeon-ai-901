# Tema 3: Diferencias y usos entre los SDKs de Microsoft Foundry (AIProjects, OpenAI, AzureOpenAI…)

### Descripción
Una de las confusiones más comunes al empezar con Foundry es: **¿qué librería instalo?** Hay un SDK para el proyecto, otro para los modelos, otros para voz, lenguaje y extracción, y además versiones viejas que siguen apareciendo en tutoriales. Este tema es tu mapa.

Analogía: el **SDK de proyectos** (`azure-ai-projects`) es la **recepción del edificio**: te identifica, te da acceso a todas las oficinas (agentes, conexiones, índices) y te entrega un pase para hablar con los modelos. El **SDK de OpenAI** es ese **pase**: con él hablas directamente con los modelos. Los SDKs de Speech, Language o Content Understanding son **oficinas especializadas** con su propia ventanilla.

### Aspectos Clave

1. **Mapa general de SDKs (Python):**

   | Paquete | Clase principal | ¿Para qué? | Estado |
   |---|---|---|---|
   | `azure-ai-projects` (2.x) | `AIProjectClient` | **SDK de Foundry**: agentes, conexiones, deployments, datasets, índices, evaluaciones; te da un cliente OpenAI autenticado con `get_openai_client()` | ✅ Recomendado |
   | `openai` | `OpenAI` | Hablar con modelos: **Responses API**, embeddings, imágenes, conversaciones | ✅ Recomendado (con endpoint `/openai/v1/`) |
   | `openai` | `AzureOpenAI` | Igual que arriba, pero estilo anterior: requiere `api_version` y `azure_endpoint` | ⚠️ Legado; con la API v1 usa `OpenAI` |
   | `azure-identity` | `DefaultAzureCredential` | Autenticación con Microsoft Entra ID (sin llaves) | ✅ |
   | `azure-ai-textanalytics` | `TextAnalyticsClient` | **Azure Language**: idioma, PII, entidades, sentimiento, frases clave | ✅ |
   | `azure-cognitiveservices-speech` | `SpeechConfig`, `SpeechRecognizer`, `SpeechSynthesizer` | **Azure Speech**: STT y TTS | ✅ |
   | `azure-ai-voicelive` | `connect()` | **Voice Live**: voz a voz en tiempo real por WebSocket (solo asíncrono) | ✅ |
   | `azure-ai-contentunderstanding` | `ContentUnderstandingClient` | **Content Understanding**: documentos, imágenes, audio, video | ✅ |
   | `azure-ai-evaluation` | Evaluadores | Medir groundedness, relevancia, seguridad | ✅ |
   | `agent-framework` | Agentes y *workflows* | **Microsoft Agent Framework**: orquestación multiagente (sucesor de Semantic Kernel y AutoGen) | ✅ |
   | `azure-ai-agents` | `AgentsClient` | Agentes "clásicos" (threads/runs) usados con `azure-ai-projects` 1.x | ⚠️ Versión anterior |
   | `azure-ai-inference` | `ChatCompletionsClient` | Cliente genérico para modelos no-OpenAI | ⚠️ Legado; Microsoft recomienda el SDK de OpenAI con la API v1 |

2. **Endpoints que vas a usar:**

   | Endpoint | Formato | Lo usa |
   |---|---|---|
   | Proyecto | `https://<recurso>.services.ai.azure.com/api/projects/<proyecto>` | `AIProjectClient` |
   | Modelos (OpenAI v1) | `https://<recurso>.openai.azure.com/openai/v1/` | `OpenAI(base_url=...)` |
   | Foundry Tools | `https://<recurso>.cognitiveservices.azure.com/` | Language, Speech |
   | Content Understanding | `https://<recurso>.services.ai.azure.com/` | `ContentUnderstandingClient` |

3. **Tres formas de llamar al mismo modelo:**

   **a) Con el SDK de Foundry + Entra ID (recomendada para producción):**
   ```python
   # pip install "azure-ai-projects>=2.0.0" openai azure-identity
   import os
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient

   project_client = AIProjectClient(
       endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
       credential=DefaultAzureCredential(),
   )
   openai_client = project_client.get_openai_client()      # cliente OpenAI ya autenticado

   r = openai_client.responses.create(model=os.environ["FOUNDRY_MODEL_NAME"],
                                      input="Explica qué es un token en una oración.")
   print(r.output_text)
   ```

   **b) Con el SDK de OpenAI + API key (la más sencilla para aprender):**
   ```python
   # pip install openai
   import os
   from openai import OpenAI

   client = OpenAI(
       base_url=os.environ["AZURE_OPENAI_ENDPOINT"],   # https://<recurso>.openai.azure.com/openai/v1/
       api_key=os.environ["FOUNDRY_KEY"],
   )
   r = client.responses.create(model=os.environ["FOUNDRY_MODEL_NAME"],
                               input="Explica qué es un token en una oración.")
   print(r.output_text)
   ```

   **c) Con REST puro (lo que hacen los SDKs por debajo):**
   ```bash
   curl -X POST "https://<recurso>.services.ai.azure.com/api/projects/<proyecto>/openai/responses?api-version=2025-11-15-preview" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $AUTH_TOKEN" \
     -d '{"model": "gpt-4.1-mini", "input": "Explica qué es un token en una oración."}'
   ```
   - **Explicación:** las tres hacen lo mismo. El SDK de Foundry agrega autenticación con Entra ID y acceso a todo el proyecto (agentes, conexiones); el SDK de OpenAI es más directo; REST sirve para cualquier lenguaje o para depurar.

4. **Responses API vs. Chat Completions:**

   | | Chat Completions (`chat.completions.create`) | Responses API (`responses.create`) |
   |---|---|---|
   | Entrada | `messages=[...]` | `input=` (texto o lista de mensajes) + `instructions=` |
   | Salida | `choices[0].message.content` | `output_text` (atajo) y `output` (lista de elementos) |
   | Estado | Tú reenvías todo el historial | Puede encadenar con `previous_response_id` o `conversation` |
   | Herramientas | Function calling | Herramientas integradas (image_generation, MCP, file_search...) |
   | En Foundry | Compatible | **La que usa Microsoft Learn y el examen** |

5. **¿Qué SDK elijo? (regla rápida):**
   - ¿Vas a crear o llamar **agentes**, usar conexiones o índices del proyecto? → `azure-ai-projects`.
   - ¿Solo quieres mandar prompts a un modelo desplegado? → `openai` (o el cliente que te da `get_openai_client()`).
   - ¿Necesitas resultados **deterministas** de texto (idioma, PII)? → `azure-ai-textanalytics`.
   - ¿Voz? → `azure-cognitiveservices-speech`; ¿voz a voz en tiempo real? → `azure-ai-voicelive`.
   - ¿Extraer campos de documentos, audio o video? → `azure-ai-contentunderstanding`.
   - ¿Orquestar varios agentes con flujos complejos? → `agent-framework`.

### Autenticación: llave vs. Entra ID

| | API key | Microsoft Entra ID (`DefaultAzureCredential`) |
|---|---|---|
| Configuración | Copiar llave del portal | `az login` en local; identidad administrada en Azure |
| Seguridad | Si se filtra, cualquiera la usa | Basado en roles (RBAC), sin secretos en el código |
| Permisos granulares | No | Sí (ej. rol **Foundry User**) |
| Recomendado para | Aprender, prototipos | Producción |

### Recursos
- [SDK de Foundry para Python (azure-ai-projects)](https://learn.microsoft.com/es-es/python/api/overview/azure/ai-projects-readme)
- [Muestras oficiales de azure-ai-projects en GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples)

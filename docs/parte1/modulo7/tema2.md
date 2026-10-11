# Tema 2: Grounding y métricas de evaluación

### Descripción
**Grounding (fundamentación)** significa que cada afirmación de la respuesta está **respaldada por el contenido recuperado**. Un RAG puede fallar en dos lugares: en la **recuperación** (no encontró la información correcta) o en la **generación** (encontró la información pero el modelo la usó mal o inventó). Por eso se evalúan por separado.

Analogía: un alumno que hace un ensayo con fuentes. La recuperación es si sacó los **libros correctos** de la biblioteca; la generación es si **citó correctamente** y no inventó datos que no estaban en esos libros.

### Aspectos Clave

1. **Grounding en la práctica:**
   - Instrucciones explícitas: "responde solo con el contexto", "si no está, dilo", "cita la fuente".
   - Citas o enlaces para que el usuario pueda verificar.
   - El grounding **reduce** las respuestas sin respaldo, pero **no las elimina**: el modelo puede malinterpretar el contexto y el buscador puede traer información incompleta.
   - En escenarios de alto impacto: revisión humana.

2. **Métricas de recuperación (¿trajo lo correcto?):**

   | Métrica | Pregunta | Cómo se mide |
   |---|---|---|
   | **Relevancia** | ¿Los fragmentos atienden la pregunta? | Juicio humano o LLM-juez |
   | **Cobertura (recall)** | ¿Está toda la info necesaria? | `% de pasajes esperados recuperados` |
   | **Ranking** | ¿Los mejores van primero? | MRR, nDCG |
   | **Precisión@k** | De los k recuperados, ¿cuántos sirven? | `relevantes en top-k / k` |
   | **Seguridad y frescura** | ¿El contenido está autorizado y vigente? | Filtros de permisos y fechas |

3. **Métricas de generación (¿respondió bien?):**

   | Métrica | Pregunta |
   |---|---|
   | **Groundedness (fundamentación)** | ¿Cada afirmación está respaldada por el contexto? |
   | **Relevancia** | ¿Responde directamente a la pregunta? |
   | **Completitud** | ¿Incluye la información importante del contexto? |
   | **Calidad de citas** | ¿Las citas apuntan a fuentes que respaldan lo dicho? |
   | **Incertidumbre apropiada** | ¿Evita adivinar cuando no hay contexto suficiente? |
   | **Coherencia y fluidez** | ¿Se lee natural y lógico? |

   Microsoft Foundry también menciona métricas de NLP tradicionales (exactitud, precisión, recall, F1) y métricas **asistidas por IA** (groundedness, relevancia, coherencia, fluidez, similitud).

4. **Conjunto de pruebas (test set):**
   - Preguntas realistas + pasajes esperados + criterio de respuesta aceptable.
   - Incluye casos difíciles: preguntas ambiguas, preguntas **sin respuesta** en los datos, documentos desactualizados, intentos de obtener información no autorizada.

5. **Calidad vs. latencia vs. costo:**
   - Más fragmentos = más cobertura, pero prompts más largos, más lentos y más caros.
   - Demasiado contexto puede **distraer** al modelo de la evidencia relevante.
   - Monitorea el uso real y **re-evalúa** cada vez que cambien datos, modelos, prompts o configuración de búsqueda.

6. **Diagnóstico rápido:**

   | Síntoma | Probable causa | Arreglo |
   |---|---|---|
   | La respuesta correcta no está en los fragmentos | Recuperación | Mejorar chunking, metadatos, búsqueda híbrida, re-ranking |
   | Está en los fragmentos pero la respuesta es incorrecta | Generación | Mejorar instrucciones, modelo más capaz, menos ruido |
   | Inventa cuando no hay información | Falta de instrucciones de incertidumbre | "Si no está en el contexto, di que no lo sabes" |
   | Cita una fuente que no dice eso | Calidad de citas | Pedir citas por afirmación; evaluar con LLM-juez |

### Práctica: evaluar groundedness con un LLM como juez
```python
import os, json
from openai import OpenAI

client = OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["FOUNDRY_KEY"])

def evaluar_groundedness(contexto, respuesta):
    prompt = f"""Evalúa si la RESPUESTA está completamente respaldada por el CONTEXTO.
Devuelve SOLO un JSON: {{"puntaje": 1-5, "afirmaciones_sin_respaldo": [..]}}
5 = todo respaldado, 1 = mayormente inventado.

CONTEXTO: {contexto}
RESPUESTA: {respuesta}"""
    r = client.responses.create(model=os.environ["FOUNDRY_MODEL_NAME"], input=prompt, temperature=0)
    return json.loads(r.output_text)

contexto = "Hospedaje internacional: hasta 180 USD por noche."
print(evaluar_groundedness(contexto, "Te pagan hasta 180 USD por noche y también el desayuno."))
# Esperado: puntaje ~2-3, afirmaciones_sin_respaldo: ["también el desayuno"]
```
- **Explicación:**
  - Un segundo modelo actúa como **juez** y detecta afirmaciones que no están en el contexto.
  - `temperature=0` hace la evaluación más consistente.
  - En producción usa los **evaluadores integrados de Microsoft Foundry** (Groundedness, Relevance, Coherence, Fluency) con el paquete `azure-ai-evaluation`, que ya traen prompts calibrados.

> [!NOTE]
> Si usas un modelo de razonamiento (por ejemplo de la familia GPT-5), algunos no aceptan `temperature`; en ese caso elimina el parámetro.

### Recursos
- [Evaluadores de Microsoft Foundry](https://learn.microsoft.com/es-es/azure/foundry/concepts/observability)
- [RAGAS: framework open source para evaluar RAG](https://docs.ragas.io/)

# Tema 1: Un agente de IA con un LLM no siempre es la solución — Por qué y cuándo usar los otros modelos de texto, visión y voz de Microsoft Foundry

### Descripción
La tentación actual es resolver todo con "un agente con GPT". Pero Foundry incluye **Foundry Tools**: servicios con modelos preentrenados y especializados que, para tareas bien definidas, son **más predecibles, baratos, rápidos y fáciles de auditar** que un LLM. Microsoft Learn lo dice explícitamente: si el caso de uso está bien definido, considera una Foundry Tool en lugar de un modelo del catálogo.

Analogía: un LLM es un **médico general** brillante; puede opinar de todo. Pero para una radiografía prefieres al **radiólogo** (servicio especializado): es más preciso, más rápido y su reporte siempre tiene el mismo formato.

### Aspectos Clave

1. **LLM vs. servicio especializado:**

   | Criterio | LLM / agente | Foundry Tool especializada |
   |---|---|---|
   | Salida | Texto libre; varía entre llamadas | **Estructurada (JSON) y determinista** |
   | Confianza | No da un puntaje calibrado | Devuelve **confidence score** |
   | Costo | Por token (entrada + salida) | Por transacción / por minuto de audio; suele ser menor |
   | Latencia | Mayor | Menor |
   | Configuración | Prompt | Ninguna (o entrenamiento personalizado) |
   | Flexibilidad | Altísima | Limitada a su tarea |
   | Auditoría y cumplimiento | Difícil de explicar | Comportamiento documentado y predecible |
   | Riesgo de alucinación | Sí | No inventa campos |

2. **Mapa de servicios especializados en Foundry:**

   | Necesidad | Servicio | Ejemplo |
   |---|---|---|
   | Detectar idioma | Azure Language | Enrutar tickets por idioma |
   | Detectar y ocultar PII | Azure Language | Anonimizar transcripciones antes de guardarlas |
   | Entidades, sentimiento, frases clave, resumen | Azure Language | Analizar 1 millón de reseñas al mes |
   | Entender intenciones (CLU) y responder FAQs | Azure Language | Bot de soporte con intents fijos |
   | Traducir texto o documentos | Azure Translator | Traducir manuales conservando formato |
   | Transcribir audio | Azure Speech (STT) | Subtítulos, transcripción por lotes de call center |
   | Generar voz | Azure Speech (TTS) | Voces neuronales para un IVR |
   | Leer texto en imágenes (OCR) | Azure Vision / Document Intelligence | Digitalizar archivo histórico |
   | Extraer campos de facturas, recibos, IDs | Document Intelligence / Content Understanding | Cuentas por pagar automatizadas |
   | Extraer información de audio y video | Content Understanding | Resumen y acciones de grabaciones de reuniones |
   | Moderar contenido | Azure Content Safety | Filtrar comentarios ofensivos |

3. **Cuándo SÍ usar un LLM / agente:**
   - Tareas **abiertas** o que combinan varios pasos ("lee esta reseña, tradúcela, resume y propón una respuesta al cliente").
   - Categorías que cambian seguido o que defines en lenguaje natural.
   - Conversación, razonamiento, redacción.

4. **El mejor patrón: combinarlos**
   - El **agente** orquesta; las **Foundry Tools** hacen el trabajo especializado como **herramientas** (por ejemplo, vía el servidor MCP de Azure Language).
   - Ejemplo: un agente de soporte detecta el idioma con Azure Language, oculta la PII, consulta la base de conocimiento y redacta la respuesta con el LLM.

### Práctica: el mismo análisis con LLM y con Azure Language
```python
# pip install openai azure-ai-textanalytics python-dotenv
import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

load_dotenv()
texto = "María García llamó desde el 55 1234 5678 para pedir que enviaran los documentos a Av. Reforma 222, CDMX."

# --- Opción A: LLM (flexible, salida variable) ---
llm = OpenAI(base_url=os.getenv("AZURE_OPENAI_ENDPOINT"), api_key=os.getenv("API_KEY"))
r = llm.responses.create(
    model=os.getenv("MODEL_DEPLOYMENT_NAME"),
    instructions="Detecta el idioma y los datos personales. Responde en JSON.",
    input=texto,
)
print("LLM:", r.output_text)

# --- Opción B: Azure Language (estructurado y determinista) ---
lang = TextAnalyticsClient(endpoint=os.getenv("AZURE_LANGUAGE_ENDPOINT"),
                           credential=AzureKeyCredential(os.getenv("API_KEY")))

idioma = lang.detect_language([texto])[0]
print(f"Idioma: {idioma.primary_language.name} ({idioma.primary_language.iso6391_name}) "
      f"confianza={idioma.primary_language.confidence_score:.2f}")

pii = lang.recognize_pii_entities([texto], language="es")[0]
print("Texto redactado:", pii.redacted_text)
for e in pii.entities:
    print(f"  {e.text} | categoría={e.category} | confianza={e.confidence_score:.2f}")

# --- Bonus: sentimiento y frases clave ---
sent = lang.analyze_sentiment(["El hotel estaba precioso pero el servicio fue lentísimo."], language="es")[0]
print("Sentimiento:", sent.sentiment, sent.confidence_scores)
frases = lang.extract_key_phrases(["El hotel estaba precioso pero el servicio fue lentísimo."], language="es")[0]
print("Frases clave:", frases.key_phrases)
```
`.env`:
```bash
AZURE_OPENAI_ENDPOINT=https://<recurso>.openai.azure.com/openai/v1/
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
AZURE_LANGUAGE_ENDPOINT=https://<recurso>.cognitiveservices.azure.com/
API_KEY=<tu-llave-de-foundry>
```
- **Explicación:**
  - Con el **LLM**, corre el script varias veces: el formato del JSON puede cambiar.
  - Con **Azure Language**, la respuesta siempre tiene la misma estructura: `primary_language.name`, `iso6391_name`, `confidence_score`, `redacted_text` (por ejemplo `**** ****** llamó desde el ************* ...`), `entities` con `category` (Person, PhoneNumber, Address) y confianza.
  - La misma llave de tu **recurso de Foundry** sirve para ambos: el recurso ya incluye Azure Language.

## Práctica oficial de Microsoft Learn
- [Ejercicio: Introducción al análisis de texto en Microsoft Foundry](https://learn.microsoft.com/es-es/training/modules/get-started-text-analysis-azure/5-exercise)
- [Ejercicio: Explorar el análisis de texto](https://learn.microsoft.com/es-es/training/modules/introduction-language/4b-exercise)

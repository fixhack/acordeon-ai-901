# Tema 1: Cómo elegir el modelo de IA adecuado para los requerimientos

### Descripción
El catálogo de Foundry tiene **más de mil modelos**. Elegir bien impacta la calidad, la latencia y, sobre todo, el costo. La selección empieza por tu **carga de trabajo, el tipo de tarea y tus restricciones** (presupuesto, latencia, idioma, cumplimiento, región).

Analogía: elegir un modelo es como elegir un vehículo. No vas por las tortillas en un tráiler ni mudas una casa en motoneta. Un modelo enorme de razonamiento es el tráiler: potente pero caro y lento para tareas simples.

### Aspectos Clave

1. **Proceso de selección en 5 pasos:**
   1. **Define la tarea:** chat, código, resumen, embeddings, visión, voz, extracción.
   2. **¿Existe una Foundry Tool?** Si el caso está bien definido (detectar idioma, PII, OCR, transcribir), un servicio especializado es más predecible, barato y rápido.
   3. **Filtra el catálogo:** por proveedor, capacidades, tarea de inferencia, licencia, región.
   4. **Compara:** *leaderboards* (calidad, seguridad, throughput, costo) y **Benchmarks → Try with your own data**.
   5. **Evalúa con tus datos:** un conjunto de prompts reales y evaluadores (groundedness, relevancia, coherencia).

2. **Tabla de modelos recomendados por tarea (según Microsoft Learn):**

   | Tarea | Modelos recomendados | Fortaleza |
   |---|---|---|
   | Chat | GPT-5.x chat, Claude Sonnet/Opus, Mistral-Large-3, DeepSeek V3.1, SLMs (Phi-4, Llama) | Razonamiento, conversación, seguridad |
   | Código | GPT-5.1-codex, Claude Sonnet | Flujos de agente complejos |
   | Resumen | GPT-5.x de razonamiento, Claude Opus/Sonnet | Contexto largo, compresión de calidad |
   | Embeddings | `text-embedding-3-small` u otros | Vectores semánticos |
   | Multimodal | Phi-4-multimodal-instruct, GPT-5.x multimodal, Mistral-Large-3 | Imágenes, audio y video en el chat |
   | Imágenes | GPT-Image-1.5, GPT-Image-1, GPT-Image-1-Mini, FLUX | Texto a imagen y edición |
   | Video | Sora, Sora 2 | Texto/imagen a video |
   | Dominio específico | Modelos ajustados por industria | Finanzas, salud, legal |

3. **Criterios de decisión:**

   | Criterio | Pregunta | Implicación |
   |---|---|---|
   | **Calidad** | ¿Qué tan difícil es la tarea? | Razonamiento complejo → modelos grandes / de razonamiento |
   | **Latencia** | ¿El usuario espera en tiempo real? | Modelos *mini/nano* o SLMs |
   | **Costo** | ¿Cuántas llamadas al día? | Alto volumen → modelo más pequeño; o despliegue *batch* |
   | **Ventana de contexto** | ¿Cuánto texto entra en cada llamada? | Contratos largos → modelos de contexto amplio |
   | **Modalidad** | ¿Entran imágenes, audio? | Modelo multimodal |
   | **Idioma** | ¿Español de México? | Prueba con tus propios datos |
   | **Cumplimiento** | ¿Dónde deben residir los datos? | Región y tipo de despliegue (*Data Zone* / regional) |
   | **Licencia** | ¿Open source o propietario? | Afecta uso comercial y opciones de hosting |
   | **Disponibilidad** | ¿Está en mi región? ¿Requiere registro? | GPT-5 requiere registro |

4. **Tipos de despliegue y parámetros:**
   - **Standard / Global Standard:** pagas por token; Global enruta a la capacidad disponible en el mundo.
   - **Provisioned (PTU):** capacidad reservada; latencia predecible para producción de alto volumen.
   - **Global Batch:** procesamiento asíncrono por lotes, más barato; para tareas que no son urgentes.
   - **TPM (tokens por minuto):** límite de velocidad que también define el RPM. Prompts grandes y `max_output_tokens` alto consumen TPM más rápido y provocan **throttling (429)**.

5. **Parámetros de inferencia:**

   | Parámetro | Efecto | Valor típico |
   |---|---|---|
   | `temperature` | Creatividad vs. determinismo | 0–0.3 para extracción/clasificación; 0.7–1 para creatividad |
   | `top_p` | Muestreo por probabilidad acumulada | Ajusta este **o** la temperatura, no ambos |
   | `max_output_tokens` | Longitud máxima de la respuesta | Limítalo para controlar costo y throttling |
   | `instructions` | System prompt | Rol, tono, reglas, formato |
   | `reasoning.effort` | Cuánto "piensa" un modelo de razonamiento | low / medium / high |

   > [!NOTE]
   > Algunos modelos de razonamiento no aceptan `temperature` o `top_p`. Revisa la ficha del modelo.

### Práctica: compara dos modelos con tus propios prompts
```python
import os, time
from openai import OpenAI

client = OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["FOUNDRY_KEY"])

prompts = [
    "Clasifica el sentimiento (positivo/negativo/neutro): 'El envío llegó tarde pero el producto es excelente'",
    "Resume en una oración: La política de viáticos permite hasta 180 USD por noche en viajes internacionales...",
]
deployments = ["gpt-4.1-mini", "gpt-4.1-nano"]   # nombres de TUS deployments

for d in deployments:
    for p in prompts:
        inicio = time.perf_counter()
        r = client.responses.create(model=d, input=p, max_output_tokens=100)
        ms = (time.perf_counter() - inicio) * 1000
        print(f"[{d}] {ms:6.0f} ms | tokens: {r.usage.input_tokens}+{r.usage.output_tokens} | {r.output_text[:80]}")
```
- **Explicación:** mides **latencia**, **tokens consumidos** (costo) y **calidad** de la respuesta con prompts reales de tu caso de uso. Así decides con datos, no con intuición.

### Para el examen
- "Necesitas el menor costo para clasificar millones de reseñas sin urgencia" → modelo pequeño + **Global Batch**.
- "Necesitas detectar el idioma de forma consistente" → **Azure Language** (Foundry Tool), no un LLM.
- "Necesitas capacidad garantizada y latencia predecible" → **Provisioned throughput**.

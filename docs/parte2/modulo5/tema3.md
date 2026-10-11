# Tema 3: Tutorial de implementación con el SDK de Python de un modelo de generación de imágenes

**Objetivo:** Generar imágenes desde código con un modelo GPT-Image desplegado en Foundry, guardarlas como PNG y editarlas iterativamente.

Lectura oficial: [Modelos de generación de imágenes – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/get-started-vision-azure/3-image-generation?pivots=text)

## Paso a Paso:

### 1. Elegir y desplegar el modelo

| Modelo | Cuándo |
|---|---|
| **GPT-Image-1.5** | Recomendado para proyectos nuevos: mejor calidad, texto a imagen, imagen a imagen y edición precisa |
| **GPT-Image-1** | Propósito general, ampliamente soportado (Responses API, herramientas de agentes) |
| **GPT-Image-1-Mini** | Menor costo y latencia |
| **FLUX** (Black Forest Labs) | Alternativa open source de terceros |

- Despliégalo desde el catálogo y pruébalo en el **Playground de imágenes**.

> [!IMPORTANT]
> GPT-Image-1 y GPT-Image-1.5 son de **acceso limitado**: hay que solicitar acceso ([GPT-Image-1](https://aka.ms/oai/gptimage1access), [GPT-Image-1.5](https://aka.ms/oai/gptimage1.5access)). La documentación de Azure ya lista versiones más nuevas como **GPT-image-2**, disponible de forma general sin registro. El examen se basa en lo que dice Microsoft Learn, pero para tus prácticas usa lo que tengas disponible en el catálogo; el código es el mismo cambiando el nombre del deployment.

### 2. Preparar el entorno
```bash
pip install openai python-dotenv
```
`.env`:
```bash
ENDPOINT=https://<recurso>.openai.azure.com/openai/v1/
FOUNDRY_KEY=<tu-llave>
MODEL_NAME=gpt-5                   # modelo de chat que orquesta la herramienta (ver nota)
IMAGE_MODEL_NAME=gpt-image-1       # nombre de TU deployment de imágenes
```

### 3. Generar una imagen con la Responses API (`generar_imagen.py`)
Este es el patrón que muestra Microsoft Learn: pedirle a la Responses API que use la herramienta `image_generation`.
```python
import os, base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["FOUNDRY_KEY"], base_url=os.environ["ENDPOINT"])

prompt = ("Ilustración plana y moderna de un ajolote programando en una laptop, "
          "estilo vectorial limpio, colores pastel, fondo con papel picado.")

response = client.responses.create(
    model=os.environ["MODEL_NAME"],
    input=prompt,
    tools=[{"type": "image_generation"}],
    extra_headers={"x-ms-oai-image-generation-deployment": os.environ["IMAGE_MODEL_NAME"]},
)

# La imagen llega en base64 dentro del elemento de tipo "image_generation_call"
imagen_b64 = next(item.result for item in response.output if item.type == "image_generation_call")

with open("ajolote.png", "wb") as f:
    f.write(base64.b64decode(imagen_b64))
print("Guardada: ajolote.png")
```
- **Explicación:**
  - `tools=[{"type": "image_generation"}]` habilita la herramienta de generación de imágenes.
  - El resultado **no es una URL** sino **base64** en `item.result` del elemento `image_generation_call`; se decodifica y se guarda.
  - **Nota sobre el `model`:** en Azure, la herramienta de imágenes la **orquesta un modelo de chat compatible** (la documentación de Foundry usa `gpt-5` como ejemplo; ambos deployments deben estar en el mismo proyecto) y el header `x-ms-oai-image-generation-deployment` indica qué deployment de GPT-Image genera la imagen. El ejemplo simplificado de Microsoft Learn pone directamente el deployment de imágenes en `model`; si tu configuración no acepta una forma, prueba la otra o copia el código del Playground.

### 4. Generar con la Images API (control de tamaño y calidad) (`images_api.py`)
```python
import os, base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["FOUNDRY_KEY"], base_url=os.environ["ENDPOINT"])

resultado = client.images.generate(
    model=os.environ["IMAGE_MODEL_NAME"],
    prompt="Póster minimalista del Palacio de Bellas Artes al atardecer, estilo art déco",
    size="1024x1536",        # vertical; también 1024x1024 o 1536x1024
    quality="medium",        # low | medium | high
    n=1,
)

with open("bellas_artes.png", "wb") as f:
    f.write(base64.b64decode(resultado.data[0].b64_json))
print("Guardada: bellas_artes.png")
```
- **Explicación:**
  - `images.generate` llama directo al modelo de imágenes y te da control de **tamaño**, **calidad** y **número** de imágenes.
  - Los modelos GPT-Image devuelven `b64_json`.
  - Mayor calidad y tamaño = más tokens = más costo y latencia.

### 5. Editar iterativamente (imagen a imagen)
Con la Responses API puedes encadenar respuestas y pedir cambios sobre la imagen anterior:
```python
r2 = client.responses.create(
    model=os.environ["MODEL_NAME"],
    previous_response_id=response.id,          # la respuesta del paso 3
    input="Ahora ponle lentes y una taza de café de olla junto a la laptop.",
    tools=[{"type": "image_generation"}],
    extra_headers={"x-ms-oai-image-generation-deployment": os.environ["IMAGE_MODEL_NAME"]},
)
imagen_b64 = next(i.result for i in r2.output if i.type == "image_generation_call")
open("ajolote_v2.png", "wb").write(base64.b64decode(imagen_b64))
```

## Tips de prompts para imágenes
- **Sujeto + acción + entorno + estilo + iluminación + composición**: "Un colibrí (sujeto) bebiendo de una flor de cempasúchil (acción) en un jardín (entorno), fotografía macro (estilo), luz dorada de tarde (iluminación), fondo desenfocado (composición)".
- Si necesitas **texto dentro de la imagen**, escríbelo entre comillas y en pocas palabras.
- Sé explícito en lo que **no** quieres: "sin texto", "sin personas".
- Itera: cambia una variable a la vez.

## IA responsable
- Los modelos bloquean contenido dañino, personas reales y material con derechos de autor.
- Informa cuando una imagen fue generada con IA (**transparencia**).
- Revisa sesgos en las representaciones de personas.

## Práctica oficial de Microsoft Learn
- [Ejercicio: Introducción a computer vision en Microsoft Foundry](https://learn.microsoft.com/es-es/training/modules/get-started-vision-azure/5-exercise)

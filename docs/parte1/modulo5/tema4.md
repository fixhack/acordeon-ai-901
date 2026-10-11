# Tema 4: Vision Transformers y modelos multimodales — Fundamentos técnicos

### Descripción
Los **Transformers** revolucionaron el lenguaje y luego la visión. Un **Vision Transformer (ViT)** trata una imagen como si fuera una oración: la corta en **parches** (como si fueran tokens) y usa **atención** para entender cómo se relacionan. Cuando además se entrena con pares imagen–texto, se obtiene un **modelo multimodal** que puede describir imágenes o responder preguntas sobre ellas.

Analogía: una CNN es como leer una página con una lupa, cuadrito por cuadrito. Un ViT es como ver la página completa de un vistazo y conectar ideas de distintas partes al mismo tiempo.

### Aspectos Clave

1. **Del texto a la imagen:**
   - En lenguaje: texto → tokens → embeddings → atención.
   - En visión: imagen → **parches** (por ejemplo de 16×16 píxeles) → vectores lineales → atención.
   - Una imagen de 224×224 se divide en 14 × 14 = **196 parches**, cada uno tratado como un "token visual".

2. **Cómo funciona un ViT:**
   1. **Parcheo:** se corta la imagen en parches.
   2. **Proyección lineal:** cada parche (16×16×3 = 768 valores) se convierte en un vector (embedding).
   3. **Codificación posicional:** se agrega la posición de cada parche (si no, el modelo no sabría si la cabeza está arriba o abajo).
   4. **Atención:** cada parche "mira" a todos los demás y calcula su influencia según color, forma, contraste y textura.
   5. **Resultado:** un "mapa" multidimensional de características visuales donde las que aparecen juntas (un **sombrero** y una **cabeza**) quedan con vectores de dirección similar.
   - El modelo no "sabe" qué es un sombrero; aprende la **relación entre características visuales**.

3. **Modelos multimodales:**
   - Combinan un **codificador de visión** y un **codificador de lenguaje**, entrenados con millones de pares imagen–descripción.
   - **Atención cruzada (cross-modal attention):** crea una representación unificada donde los embeddings de imagen y de texto viven en el **mismo espacio vectorial**.
   - Por eso el modelo puede describir una foto que nunca vio: busca el lenguaje asociado a esas características visuales. Ejemplo de Microsoft Learn: "Una persona en un parque con sombrero y mochila".
   - **Aprendizaje contrastivo (ej. CLIP de OpenAI, 2021):** técnica popular para alinear imágenes y textos acercando los pares correctos y alejando los incorrectos en el espacio vectorial.

4. **CNN vs. ViT vs. Multimodal:**

   | | CNN | ViT | Multimodal |
   |---|---|---|---|
   | Unidad de análisis | Ventanas locales (kernels) | Parches + atención global | Parches + tokens de texto |
   | Fortaleza | Eficiente con pocos datos | Relaciones globales, escala muy bien | Entiende y genera lenguaje sobre imágenes |
   | Salida típica | Etiqueta, cajas | Etiqueta, embeddings | Texto libre, respuestas, JSON |
   | Datos necesarios | Medianos | Muchos | Enormes (pares imagen–texto) |

5. **Multimodales en Microsoft Foundry:**
   - **GPT-4.1 / 4.1-mini / 4.1-nano:** describir imágenes, preguntas visuales, analizar documentos, capturas, gráficas y diagramas.
   - **Serie GPT-5 (5.1, 5.2):** escenarios empresariales y agénticos con imágenes, salidas estructuradas y herramientas.
   - **Phi-4-multimodal-instruct** y modelos de socios (Anthropic, Mistral) con entrada de imagen.
   - Tutorial en la [Parte 2, Módulo 5](../../parte2/modulo5/tema2.md).

### Práctica: ver los embeddings de imagen y texto en el mismo espacio (CLIP)
```python
# pip install transformers torch pillow requests
from PIL import Image
import requests
from transformers import CLIPModel, CLIPProcessor

modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

url = "http://images.cocodataset.org/val2017/000000039769.jpg"   # dos gatos en un sillón
imagen = Image.open(requests.get(url, stream=True).raw)
textos = ["una foto de gatos", "una foto de un perro", "una foto de un coche"]

entradas = procesador(text=textos, images=imagen, return_tensors="pt", padding=True)
probs = modelo(**entradas).logits_per_image.softmax(dim=1)[0]

for texto, p in zip(textos, probs):
    print(f"{texto:25s} {p:.2%}")
```
- **Explicación:**
  - `clip-vit-base-patch32` usa un **ViT** con parches de 32×32 como codificador de imagen.
  - El modelo compara el embedding de la imagen con el de cada texto; la opción "gatos" obtiene la probabilidad más alta.
  - Esto es *clasificación zero-shot*: nunca se entrenó con esas etiquetas exactas.

### Recursos
- [An Image is Worth 16x16 Words (paper ViT)](https://arxiv.org/abs/2010.11929)
- [CLIP: Connecting text and images – OpenAI](https://openai.com/index/clip/)

# Tema 5: Generación de imágenes — Fundamentos técnicos

### Descripción
La misma arquitectura multimodal que permite "preguntarle" cosas a una imagen puede funcionar **al revés**: a partir de un prompt en lenguaje natural, el modelo identifica las características visuales asociadas a esas palabras y **sintetiza una imagen nueva**. Hoy la mayoría de los generadores usan **difusión**.

Analogía: un escultor frente a un bloque de mármol. El bloque es **ruido aleatorio**; el escultor (el modelo) quita material poco a poco, guiado por la descripción ("un perro con un palo en el hocico"), hasta que aparece la figura.

### Aspectos Clave

1. **Modelos de difusión, paso a paso:**
   1. **Condicionamiento por texto:** el prompt se convierte en embeddings que identifican características visuales relacionadas.
   2. **Inicio con ruido:** la imagen comienza como un conjunto de píxeles aleatorios.
   3. **Eliminación iterativa de ruido (denoising):** en cada paso el modelo predice qué parte es ruido y lo quita, creando estructura.
   4. **Evaluación contra el prompt:** en cada iteración compara la imagen con la descripción, hasta producir la escena deseada.

2. **¿Cómo aprende a quitar ruido?**
   - **Entrenamiento (proceso hacia adelante):** se toman millones de imágenes reales con su descripción y se les agrega ruido gradualmente hasta que quedan como estática.
   - El modelo aprende la tarea inversa: **dado una imagen con ruido + el texto, predecir el ruido** que hay que quitar.
   - **Generación (proceso inverso):** se parte de ruido puro y se aplica ese aprendizaje decenas de veces.
   - **Difusión latente (Stable Diffusion):** en lugar de trabajar sobre píxeles, trabaja en un espacio comprimido (*latente*), mucho más rápido.

3. **Parámetros que verás en los generadores:**
   - **Prompt / negative prompt:** qué incluir y qué evitar.
   - **Pasos (steps):** más pasos = más detalle, más tiempo.
   - **Guidance scale (CFG):** qué tanto se apega al prompt vs. creatividad.
   - **Seed (semilla):** misma semilla + mismo prompt = misma imagen (reproducibilidad).
   - **Tamaño y calidad.**

4. **Otras arquitecturas generativas (contexto histórico):**

   | Arquitectura | Idea | Ejemplo |
   |---|---|---|
   | GAN (2014) | Un generador y un discriminador compiten | StyleGAN (rostros que no existen) |
   | VQGAN + CLIP (2021) | VQGAN genera y CLIP evalúa si la imagen coincide con el texto, optimizando iterativamente | Arte generativo de 2021 en Google Colab |
   | Difusión (2020–hoy) | Quitar ruido guiado por texto | Stable Diffusion, FLUX |
   | Generación nativa multimodal | El mismo modelo multimodal que entiende texto e imágenes también las genera (OpenAI la describe como autorregresiva) | Familia GPT-Image |

5. **Video:**
   Los modelos de video extienden la idea, pero además deben respetar el **comportamiento físico** (que un perro camine con las patas en el suelo) y la **progresión temporal** (una secuencia lógica de acciones). En Foundry: **Sora** y **Sora 2** ([Parte 2, Módulo 5](../../parte2/modulo5/tema4.md)).

6. **IA responsable en generación de imágenes:**
   - Restricciones sobre personas reales, personajes con derechos de autor y contenido dañino.
   - Riesgo de *deepfakes* y desinformación → **transparencia** (credenciales de contenido / marcas de agua C2PA).
   - Sesgos en las representaciones ("un doctor" siempre genera el mismo perfil).

### Práctica: VQGAN + CLIP en Google Colab
Antes de los modelos de difusión comerciales, uno de los primeros generadores de texto a imagen accesibles para todos fue **VQGAN + CLIP**, publicado por Katherine Crowson como notebook de Google Colab. Es excelente para **ver el proceso iterativo**: la imagen va apareciendo paso a paso mientras CLIP la "califica" contra tu prompt.

- [Notebook original de VQGAN + CLIP (Katherine Crowson) en Google Colab](https://colab.research.google.com/drive/1go6YwMFe5MX6XM9tv-cnQiSTU50N9EeT)
- [Versión mantenida en GitHub (nerdyrodent/VQGAN-CLIP)](https://github.com/nerdyrodent/VQGAN-CLIP)
- [Guía paso a paso de Adafruit para usarlo](https://learn.adafruit.com/generating-ai-art-with-vqgan-clip)

> [!WARNING]
> El notebook original está marcado como descontinuado y puede fallar con las versiones actuales de Colab. Si no corre, usa el repositorio de nerdyrodent o la práctica con difusión de abajo.

### Práctica: difusión con Hugging Face (Colab con GPU gratuita)
```python
# En Google Colab: Entorno de ejecución > Cambiar tipo > GPU T4
# !pip install diffusers transformers accelerate
import torch
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
).to("cuda")

prompt = "Un ajolote astronauta flotando sobre la Ciudad de México, ilustración estilo acuarela"
imagen = pipe(prompt=prompt, num_inference_steps=4, guidance_scale=0.0).images[0]
imagen.save("ajolote.png")
```
- **Explicación:**
  - `sdxl-turbo` es una versión destilada de Stable Diffusion XL que genera en **1–4 pasos** en lugar de 30–50.
  - `num_inference_steps` controla cuántas veces se quita ruido. Prueba 1, 2 y 4 para ver la diferencia.
  - En Foundry harás lo mismo con modelos administrados como **GPT-Image-1.5** o **FLUX**, sin necesitar GPU propia.

### Recursos
- [What are Diffusion Models? – Lilian Weng](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)
- [The Illustrated Stable Diffusion – Jay Alammar](https://jalammar.github.io/illustrated-stable-diffusion/)

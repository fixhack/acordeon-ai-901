# Tema 6: Bases técnicas de cómo funciona computer vision

### Descripción
La **visión por computadora** es el conjunto de técnicas con las que el software procesa entrada visual (imágenes, video o cámaras en vivo) para extraer información. Para la computadora, una foto es solo una **matriz de números**: cada píxel vale de 0 (negro) a 255 (blanco), y una imagen a color tiene tres capas (canales Rojo, Verde y Azul).

Analogía: imagina una hoja cuadriculada gigante donde cada cuadrito tiene un número que indica qué tan brillante es. La visión por computadora es aprender a reconocer formas buscando patrones en esa cuadrícula.

### Aspectos Clave

1. **Las cuatro tareas que debes saber distinguir:**

   | Tarea | Pregunta que responde | Salida | Ejemplo |
   |---|---|---|---|
   | **Clasificación de imágenes** | ¿Qué hay en la imagen? | Una etiqueta para toda la imagen | Báscula del súper que reconoce "manzana" |
   | **Detección de objetos** | ¿Qué objetos hay y dónde? | Etiquetas + *bounding boxes* (rectángulos) | Caja de autocobro que identifica varios productos a la vez |
   | **Segmentación semántica** | ¿A qué objeto pertenece cada píxel? | Máscara a nivel píxel | Separar con precisión la fruta del fondo |
   | **Análisis contextual (multimodal)** | ¿Qué está pasando? | Descripción en lenguaje natural o etiquetas | "Una persona comiendo una manzana" |

2. **Cómo "ve" un modelo:**
   - **Filtros (kernels):** matrices pequeñas (por ejemplo 3×3) que se deslizan por la imagen (*convolución*) para resaltar bordes, texturas o formas.
   - **CNN (redes neuronales convolucionales):** aprenden automáticamente los mejores filtros para una tarea. Fueron el estándar por años.
   - **Vision Transformers (ViT):** cortan la imagen en *parches* y usan *atención* para relacionarlos, igual que un LLM relaciona palabras.
   - **Modelos multimodales:** combinan un codificador de visión y uno de lenguaje; por eso puedes "preguntarle" cosas a una imagen.
   - **Modelos de difusión:** el camino inverso; generan imágenes a partir de texto quitando ruido paso a paso.

3. **Escenarios reales:**
   - Inventario en anaqueles, control de calidad en manufactura, lectura de placas, accesibilidad (describir imágenes a personas ciegas), análisis de imágenes médicas, moderación de contenido y generación de imágenes para marketing.

4. **Visión en Microsoft Foundry (lo que verás en la Parte 2):**
   - **Modelos multimodales** (GPT-4.1, GPT-5.x) para describir imágenes o responder preguntas sobre ellas.
   - **Modelos de generación de imágenes** (GPT-Image-1.5, GPT-Image-1, GPT-Image-1-Mini, FLUX).
   - **Modelos de video** (Sora, Sora 2).
   - **Azure Vision** y **Content Understanding** para análisis especializado y extracción de información.

### Para el examen
- Pregunta "¿dónde está?" → detección. Pregunta "¿qué es?" → clasificación. Pregunta "contorno exacto" → segmentación. Pregunta "describe la escena" → modelo multimodal.

Profundizas en el [Módulo 5](../modulo5/tema1.md).

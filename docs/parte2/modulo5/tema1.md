# Tema 1: Modelos de IA multimodales — Fundamentos técnicos

### Descripción
Un **modelo multimodal** acepta (y a veces genera) más de un tipo de dato: texto, imágenes, audio o video. En la práctica de la AI-901, "multimodal" casi siempre significa **un LLM que también ve imágenes**: le mandas una foto y una pregunta en el mismo mensaje y te responde en texto.

Analogía: un LLM de solo texto es como platicar por teléfono: solo te puede describir las cosas. Un modelo multimodal es una videollamada: le enseñas el objeto y te dice qué es.

### Aspectos Clave

1. **Cómo procesa una imagen un LLM multimodal:**
   ```
   Imagen ─► [Codificador de visión (ViT)] ─► parches → embeddings visuales ─┐
                                                                            ├─► [Transformer (LLM)] ─► texto
   Texto  ─► [Tokenizador]                 ─► embeddings de texto ──────────┘
   ```
   1. La imagen se divide en **parches** y un **Vision Transformer** los convierte en embeddings.
   2. Un **proyector** los lleva al mismo espacio vectorial que los tokens de texto.
   3. El LLM los procesa juntos con **atención**: cada palabra de tu pregunta puede "mirar" a cada parche de la imagen.
   4. El decodificador genera la respuesta token por token.

2. **Tokens de imagen y costo:**
   - Las imágenes **también consumen tokens**, según su resolución y el nivel de detalle solicitado.
   - Una imagen grande en alta resolución puede costar cientos o miles de tokens.
   - Para ahorrar: redimensiona antes de enviar o usa detalle bajo cuando no necesites leer texto pequeño.

3. **Modalidades de entrada y salida en Foundry:**

   | Modelo / familia | Entrada | Salida |
   |---|---|---|
   | GPT-4.1, 4.1-mini, 4.1-nano | Texto, imagen | Texto |
   | GPT-5.x | Texto, imagen | Texto (estructurado, herramientas) |
   | Phi-4-multimodal-instruct | Texto, imagen, audio | Texto |
   | GPT-Image-1.5 / 1 / 1-Mini | Texto, imagen | **Imagen** |
   | Sora / Sora 2 | Texto, imagen (y video en Sora 2) | **Video** (Sora 2 también audio) |
   | Modelos de audio / realtime | Audio, texto | Audio, texto |

4. **Qué pueden hacer con imágenes:**
   - Describir escenas y generar *alt text*.
   - Responder preguntas visuales ("¿cuántas personas usan casco?").
   - Leer texto (OCR implícito), tablas, **gráficas** y **diagramas**.
   - Analizar capturas de pantalla (soporte técnico, pruebas de UI).
   - Comparar varias imágenes en el mismo mensaje.
   - Extraer datos a **JSON** con salidas estructuradas.

5. **Limitaciones:**
   - Pueden **alucinar** detalles o contar mal objetos pequeños o muy numerosos.
   - Precisión espacial limitada (no dan *bounding boxes* confiables como un detector de objetos).
   - No sustituyen servicios especializados cuando necesitas **confianza por campo**, coordenadas o procesamiento masivo y determinista (Content Understanding, Document Intelligence).
   - Restricciones de IA responsable (por ejemplo, no identifican a personas por su rostro).

6. **Multimodal vs. visión tradicional:**

   | Necesidad | Mejor opción |
   |---|---|
   | Preguntas abiertas sobre una imagen | Modelo multimodal |
   | Ubicación exacta de objetos (cajas) | Detección de objetos (Azure Vision / modelo custom) |
   | Extraer campos de 50,000 facturas con confianza | Content Understanding |
   | Describir fotos para accesibilidad | Modelo multimodal |

### Para el examen
La habilidad *"Interpret visual input in prompts by using a deployed multimodal model"* se evalúa con escenarios como: "Una app de safari debe identificar el animal de una foto subida por el usuario" → despliega un **modelo multimodal** y envía la imagen junto con el prompt.

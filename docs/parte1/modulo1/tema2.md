# Tema 2: ¿Qué es la IA realmente? Acercamiento técnico

### Descripción
En el día a día "IA" se usa como palabra mágica, pero técnicamente una IA es **una función matemática con millones (o billones) de parámetros ajustados a partir de datos**. Recibe una entrada (texto, imagen, audio), la convierte en números, hace operaciones y devuelve una salida (una etiqueta, un número, el siguiente token, una imagen).

Analogía: una receta tradicional de software es como un instructivo de IKEA donde un humano escribió cada paso. Un modelo de IA es como un chef que aprendió probando miles de platillos: nadie le escribió las reglas, las **dedujo de los ejemplos**.

### Aspectos Clave

1. **Programación tradicional vs. aprendizaje automático:**

   | | Programación tradicional | Machine learning |
   |---|---|---|
   | Entrada | Datos + **reglas** escritas por humanos | Datos + **respuestas esperadas** (o datos sin etiquetar) |
   | Salida | Respuestas | **Reglas aprendidas** (el modelo) |
   | Ejemplo | `if monto > 10000: alerta()` | Un modelo que aprende qué transacciones son fraude viendo miles de ejemplos |

2. **Un modelo es una función `y = f(x)`:**
   - `x` son las **características** (*features*): los datos de entrada convertidos en números.
   - `y` es la **etiqueta** (*label*) o la predicción.
   - `f` tiene **parámetros** (pesos) que se ajustan durante el **entrenamiento** para reducir el error.
   ```python
   # Un "modelo" de una sola neurona: predecir el precio de un taco según su tamaño
   peso, sesgo = 0.0, 0.0
   datos = [(10, 25), (15, 35), (20, 45)]   # (tamaño en cm, precio en MXN)
   tasa = 0.001

   for epoca in range(5000):
       for x, y_real in datos:
           y_pred = peso * x + sesgo          # inferencia
           error = y_pred - y_real            # qué tan mal le fue
           peso  -= tasa * error * x          # ajuste (gradiente descendente)
           sesgo -= tasa * error

   print(f"Precio estimado de un taco de 18 cm: ${peso * 18 + sesgo:.2f}")
   ```
   - **Explicación:**
     - El modelo empieza sin saber nada (pesos en cero).
     - En cada vuelta compara su predicción con el valor real y ajusta los pesos un poquito en la dirección que reduce el error. Esto es, en esencia, lo mismo que hace un LLM con billones de parámetros.

3. **Entrenamiento vs. inferencia:**
   - **Entrenamiento:** el proceso caro (GPUs, semanas, millones de dólares en modelos grandes) donde se ajustan los pesos.
   - **Inferencia:** usar el modelo ya entrenado para predecir. Es lo que haces cada vez que llamas a un endpoint de Foundry.
   - En la AI-901 **casi nunca entrenas**: consumes modelos ya entrenados (del catálogo o de Foundry Tools) y los adaptas con prompts, herramientas y datos (RAG).

4. **Todo se convierte en números:**
   - **Texto** → tokens → IDs → vectores (*embeddings*).
   - **Imágenes** → matrices de píxeles (0–255) por canal RGB.
   - **Audio** → muestras de la onda (por ejemplo 16,000 por segundo) → espectrogramas.
   La IA no "entiende" como un humano: encuentra **patrones estadísticos** en esas representaciones numéricas.

5. **La IA es probabilística:**
   - Un modelo no dice "esto es un gato"; dice "hay 92% de probabilidad de que sea gato".
   - Un LLM no "sabe" la respuesta; calcula cuál es el siguiente token más probable.
   - Por eso existen las **alucinaciones** y por eso el principio de *confiabilidad y seguridad* insiste en manejar umbrales de confianza.

6. **Las cargas de trabajo (workloads) de IA que evalúa el examen:**
   - IA generativa y agéntica
   - Análisis de texto
   - Voz
   - Visión por computadora
   - Extracción de información

### Para el examen
- Si una pregunta habla de "predecir un valor numérico" → regresión; "asignar una categoría" → clasificación; "agrupar sin etiquetas" → clustering.
- Si habla de "crear contenido nuevo a partir de lenguaje natural" → IA generativa.
- Si habla de "tomar acciones usando herramientas" → agente.

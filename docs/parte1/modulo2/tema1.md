# Tema 1: Las bases de cómo funciona la IA — Espacio vectorial, tokenización y embeddings

### Descripción
Un LLM es, en el fondo, una máquina que **predice el siguiente token**. Para hacerlo necesita convertir el lenguaje en matemáticas. Este tema recorre ese viaje: de texto a tokens, de tokens a vectores, de vectores a embeddings con contexto y, finalmente, a una predicción.

Analogía: piensa en un mapa de la Ciudad de México donde cada palabra es un lugar. "Tacos" y "taquería" están en la misma colonia; "aeropuerto" está en otra zona. Los embeddings son las **coordenadas** de cada palabra en ese mapa, pero con miles de dimensiones en lugar de dos.

### Aspectos Clave

1. **Tokenización:**
   - El texto se divide en **tokens**: palabras completas, subpalabras, signos de puntuación u otras secuencias comunes.
   - Cada token distinto recibe un **ID entero**. Si un token se repite, reutiliza su ID.

   | Token | ID |
   |---|---|
   | Escuché | 1 |
   | a | 2 |
   | un | 3 |
   | perro | 4 |
   | ladrar | 5 |

   - Prueba un tokenizador real:
     ```python
     # pip install tiktoken
     import tiktoken

     enc = tiktoken.get_encoding("o200k_base")   # tokenizador usado por modelos GPT-4o / GPT-4.1
     ids = enc.encode("Escuché a un perro ladrar muy fuerte")
     print(ids)
     print([enc.decode([i]) for i in ids])
     ```
   - **Explicación:** verás que algunas palabras en español se parten en varios tokens. Por eso un texto en español suele consumir **más tokens** que el mismo texto en inglés (y cuesta un poco más).

2. **Vectores:**
   - Cada token se asocia con un **vector**: un arreglo de números, por ejemplo `[3, 7, 10]`.
   - Cada posición del vector es una **dimensión** que codifica algún atributo lingüístico o semántico.
   - Al iniciar el entrenamiento los valores son **aleatorios**. En los modelos reales hay **miles** de dimensiones.

3. **Codificación posicional:**
   El orden importa ("el perro mordió al hombre" ≠ "el hombre mordió al perro"), así que junto al vector se agrega información de la **posición** de cada token.

4. **Atención y embeddings:**
   - La **atención** analiza cada token y calcula cuánto influyen los tokens a su alrededor.
   - En "Escuché a un perro **ladrar**", las palabras "escuché" y "perro" pesan mucho más que "a" o "un" para entender "ladrar".
   - La **atención multi-cabeza** evalúa varias dimensiones en paralelo.
   - El resultado son **embeddings**: vectores que ya incluyen el **contexto**.

5. **Espacio vectorial y similitud coseno:**
   - Si imaginas cada embedding como una flecha, los tokens con significado parecido **apuntan en la misma dirección**.
   - La cercanía se mide con la **similitud coseno**: 1 = misma dirección, 0 = sin relación, −1 = opuestos.
   ```python
   import numpy as np

   def similitud_coseno(a, b):
       return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

   perro    = np.array([10, 3, 2])
   cachorro = np.array([5, 3, 2])
   patineta = np.array([-3, -2, 2])

   print(f"perro vs cachorro: {similitud_coseno(perro, cachorro):.2f}")   # ~0.96
   print(f"perro vs patineta: {similitud_coseno(perro, patineta):.2f}")   # ~-0.73
   ```
   - **Explicación:** estos son los embeddings simplificados que usa Microsoft Learn. "Perro" y "cachorro" son muy similares; "patineta" apunta a otro lado.

6. **Transformer: codificador y decodificador:**
   ```
   Prompt → [Tokenización] → [Embeddings + posición] → ENCODER (atención) → DECODER (atención enmascarada) → siguiente token
                                                                                       ↑__________________________|
                                                                                       (se agrega y se repite)
   ```
   - **Encoder:** crea embeddings con atención + una red neuronal *feed-forward*.
   - **Decoder:** predice el siguiente token más probable.
   - **Entrenamiento:** usa **atención enmascarada**: el modelo solo ve los tokens anteriores, predice el siguiente, compara con el real y ajusta pesos.
   - **Inferencia:** predice un token, lo agrega a la secuencia y repite hasta que decide terminar. Por eso el texto "aparece" palabra por palabra en un chat.

7. **¿Por qué importa esto para un desarrollador?**
   - **Costos y límites** se miden en tokens (TPM: tokens por minuto).
   - **Ventana de contexto:** el número máximo de tokens que el modelo puede considerar a la vez.
   - **Embeddings** son la base de la **búsqueda vectorial** y del **RAG**.
   - **Temperatura:** controla qué tan "arriesgada" es la elección del siguiente token (baja = predecible, alta = creativa).

### Recursos
- [Attention Is All You Need (paper original)](https://arxiv.org/abs/1706.03762)
- [The Illustrated Transformer – Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Transformers explicados visualmente – 3Blue1Brown](https://www.youtube.com/watch?v=wjZofJX0v4M)

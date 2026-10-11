# Tema 2: Modelos de lenguaje semántico — Explicación técnica

### Descripción
El análisis estadístico no sabe que "carro" y "auto" significan lo mismo. Los **modelos semánticos** resuelven esto representando cada palabra como un **vector denso** cuyos valores se aprenden según cómo se usa la palabra. Si dos palabras aparecen en contextos parecidos, sus vectores terminan apuntando en direcciones parecidas.

Analogía: "Dime con quién andas y te diré quién eres". Una palabra se define por las palabras que la rodean (hipótesis distribucional).

### Aspectos Clave

1. **Evolución de los modelos semánticos:**

   | Generación | Ejemplo | Característica |
   |---|---|---|
   | Embeddings estáticos | Word2Vec (2013), GloVe (2014) | Un vector fijo por palabra; "banco" (de dinero) y "banco" (para sentarse) comparten vector |
   | Embeddings contextualizados | Transformers: BERT, familia GPT | El vector cambia según el contexto gracias a la **atención** |

2. **Texto como vectores (ejemplo de Microsoft Learn):**

   | Palabra | Vector |
   |---|---|
   | dog | [0.8, 0.6, 0.1] |
   | puppy | [0.9, 0.7, 0.4] |
   | cat | [0.7, 0.5, 0.2] |
   | kitten | [0.8, 0.6, 0.5] |
   | young | [0.1, 0.1, 0.3] |
   | ball | [0.3, 0.9, 0.1] |
   | tree | [0.2, 0.1, 0.9] |

3. **Similitud coseno:**
   `cos(A, B) = (A · B) / (‖A‖ × ‖B‖)`
   ```python
   import numpy as np

   v = {
       "dog": [0.8, 0.6, 0.1], "puppy": [0.9, 0.7, 0.4], "cat": [0.7, 0.5, 0.2],
       "kitten": [0.8, 0.6, 0.5], "young": [0.1, 0.1, 0.3], "ball": [0.3, 0.9, 0.1],
       "tree": [0.2, 0.1, 0.9],
   }
   v = {k: np.array(x) for k, x in v.items()}

   def cos(a, b):
       return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

   print(f"dog-cat:  {cos(v['dog'], v['cat']):.3f}")    # 0.991 (Learn lo redondea a ≈0.992) → muy similares
   print(f"dog-tree: {cos(v['dog'], v['tree']):.3f}")   # 0.333 → poco similares
   print(f"cat-tree: {cos(v['cat'], v['tree']):.3f}")   # 0.452 → poco similares
   ```
   - **Explicación:** "tree" es el intruso entre dog, cat y tree.

4. **Aritmética de vectores y analogías:**
   ```python
   def mas_cercano(vector, excluir=()):
       candidatos = {k: cos(vector, x) for k, x in v.items() if k not in excluir}
       return max(candidatos, key=candidatos.get)

   print(mas_cercano(v["dog"] + v["young"], excluir=("dog", "young")))           # puppy
   print(mas_cercano(v["kitten"] - v["puppy"] + v["dog"], excluir=("kitten", "puppy", "dog")))  # cat
   ```
   - **Explicación:**
     - `dog + young = puppy` (perro + joven = cachorro).
     - "*puppy* es a *dog* como *kitten* es a ?" → `kitten − puppy + dog = cat`.
     - En la práctica el resultado casi nunca coincide exacto, por eso se busca el **vector más cercano**.

5. **Embeddings contextualizados y atención:**
   - En "fui al **banco** a sacar dinero" y "me senté en el **banco** del parque", un Transformer genera **vectores distintos** para "banco" porque la atención pondera las palabras vecinas ("dinero" vs. "parque").
   - Estos embeddings son la base de la IA generativa moderna.

6. **Aplicaciones de análisis de texto con vectores:**
   - **Resumen:** seleccionar oraciones cuyo vector se parezca más al vector promedio del documento.
   - **Palabras clave:** palabras cuyo vector es más central o más similar al del documento.
   - **NER:** modelos ajustados que, con el embedding y su contexto, deciden si un token es persona, organización o lugar.
   - **Clasificación de textos:** promediar los embeddings del documento y usarlos como características para un clasificador (sentimiento, tema).
   - **Búsqueda semántica:** encontrar "política de hospedaje internacional" aunque el usuario escriba "¿cuánto me pagan de hotel en el extranjero?". Es el corazón del RAG.

7. **Embeddings en Microsoft Foundry:**
   Puedes desplegar un modelo de embeddings (por ejemplo `text-embedding-3-small`) y generar vectores reales:
   ```python
   import os
   from openai import OpenAI

   client = OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"],  # https://<recurso>.openai.azure.com/openai/v1/
                   api_key=os.environ["FOUNDRY_KEY"])

   resp = client.embeddings.create(model="text-embedding-3-small",   # nombre de tu deployment
                                   input=["perro", "cachorro", "patineta"])
   print(len(resp.data[0].embedding))   # 1536 dimensiones
   ```
   - **Explicación:** cada palabra se convierte en un vector de 1,536 números. Con la función `cos` de arriba puedes comparar su similitud.

### Recursos
- [Word2Vec explicado visualmente – Jay Alammar](https://jalammar.github.io/illustrated-word2vec/)
- [TensorFlow Embedding Projector (explora embeddings en 3D)](https://projector.tensorflow.org/)

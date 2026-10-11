# Tema 1: Análisis estadístico de texto — Fundamentos técnicos

### Descripción
Antes de los LLMs, el NLP se hacía **contando**. La idea central es sencilla: si una palabra aparece mucho en un documento, probablemente indica de qué trata. Estas técnicas siguen vigentes porque son rápidas, baratas, explicables y funcionan sin GPU. Además, conceptos como TF-IDF siguen vivos en la **búsqueda por palabras clave** (BM25) que se usa en el RAG híbrido.

Analogía: es como adivinar de qué trata una plática escuchando solo las palabras que más se repiten. Si oyes "gol", "portero" y "penal" muchas veces, es fútbol.

### Aspectos Clave

1. **Preprocesamiento (tokenización y normalización):**
   ```python
   import re
   from collections import Counter

   texto = """La IA está transformando los negocios. Las empresas usan IA para mejorar
   decisiones, anticipar al mercado y atender mejor al cliente. La IA da ventajas al negocio."""

   stopwords = {"la", "las", "los", "el", "y", "para", "al", "da", "está", "usan", "a", "de"}
   tokens = [t for t in re.findall(r"\w+", texto.lower()) if t not in stopwords]
   print(Counter(tokens).most_common(5))
   ```
   - **Explicación:**
     - `lower()` normaliza mayúsculas; `re.findall(r"\w+")` tokeniza y quita puntuación.
     - Se filtran *stopwords* para que no dominen el conteo.
     - Resultado: "ia" es el término más frecuente → el texto habla de IA.
   - **Limitación:** "negocios" y "negocio" se cuentan separado. Ahí entran el **stemming** o la **lematización**.

2. **Análisis de frecuencia:**
   - Cuenta y tabula términos. Funciona para un documento.
   - **Problema:** en una colección de documentos sobre IA, palabras como "IA", "Microsoft" o "agente" aparecen en todos, así que no ayudan a distinguirlos.

3. **TF-IDF (Term Frequency – Inverse Document Frequency):**
   - **TF:** cuántas veces aparece el término en el documento.
   - **IDF:** `log(N / df(t))`, donde `N` es el número de documentos y `df(t)` cuántos contienen el término.
   - **TF-IDF:** `tf × idf`. Un término que está en **todos** los documentos tiene `idf = log(1) = 0`.
   ```python
   # pip install scikit-learn
   from sklearn.feature_extraction.text import TfidfVectorizer

   docs = [
       "Crea agentes declarativos con Copilot Studio sin escribir código. Copilot Studio es low-code.",
       "Desarrolla agentes con código en Microsoft Foundry usando Python y el SDK de Foundry.",
   ]
   vec = TfidfVectorizer()
   matriz = vec.fit_transform(docs)
   terminos = vec.get_feature_names_out()

   for i, doc in enumerate(matriz.toarray()):
       top = sorted(zip(terminos, doc), key=lambda x: -x[1])[:3]
       print(f"Documento {i+1}: {top}")
   ```
   - **Explicación:** "agentes" aparece en ambos documentos, así que pesa poco. "copilot" y "studio" destacan en el primero; "foundry" en el segundo. Igual que el ejemplo de Microsoft Learn: el documento A trata de Copilot Studio y el B de Microsoft Foundry.
   - **Nota:** scikit-learn usa una variante suavizada del IDF, por eso los valores no son exactamente `tf × ln(N/df)`, pero la intuición es la misma.

4. **Bolsa de palabras (Bag of Words) y Naive Bayes:**
   - **Bolsa de palabras:** representa un texto como un vector de conteos, **ignorando gramática y orden**.
   - **Naive Bayes:** clasificador probabilístico que aplica el teorema de Bayes para predecir la clase según la frecuencia de palabras.
   ```python
   from sklearn.feature_extraction.text import CountVectorizer
   from sklearn.naive_bayes import MultinomialNB

   textos = ["cura milagrosa baja de peso rápido", "reunión de equipo mañana a las 10",
             "anti edad milagro oferta", "te comparto la minuta de la junta"]
   etiquetas = ["spam", "ok", "spam", "ok"]

   vectorizador = CountVectorizer()
   X = vectorizador.fit_transform(textos)
   modelo = MultinomialNB().fit(X, etiquetas)

   print(modelo.predict(vectorizador.transform(["oferta milagrosa para bajar de peso"])))  # ['spam']
   ```
   - **Explicación:** el modelo aprende qué palabras son típicas de cada clase. El mismo método sirve para **análisis de sentimiento** (positivo/negativo).

5. **TextRank:**
   - Algoritmo **no supervisado basado en grafos**, inspirado en PageRank de Google.
   - **Idea:** "una oración es importante si se parece a muchas otras oraciones importantes".
   - **Pasos:**
     1. Construir un grafo: oraciones = nodos; aristas = similitud (traslape de palabras o similitud coseno).
     2. Calcular el rango iterativamente: `TR(Si) = (1 − d) + d × Σ (wji / Σ wjk) × TR(Sj)`, con `d ≈ 0.85`.
     3. Tomar las oraciones con mayor puntaje como **resumen extractivo**.
   - A nivel palabra (palabras = nodos, aristas = co-ocurrencia) sirve para **extracción de palabras clave**.

### Resumen extractivo vs. abstractivo

| | Extractivo | Abstractivo |
|---|---|---|
| Qué hace | Copia las oraciones más relevantes | Genera texto nuevo |
| Técnica | TextRank, puntajes estadísticos | Modelos semánticos / LLMs |
| Ventaja | Fiel al original, barato | Natural, conciso |
| Riesgo | Puede quedar incoherente | Puede alucinar |

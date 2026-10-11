# Tema 4: Bases técnicas de cómo funciona el análisis de texto y el lenguaje natural

### Descripción
El **procesamiento de lenguaje natural (NLP)** es la rama de la IA que permite a las computadoras analizar texto para inferir significado. Para una computadora, "Me encantó el servicio" es solo una cadena de caracteres; el NLP la convierte en números con los que se puede calcular algo útil: sentimiento, idioma, entidades, temas o un resumen.

Analogía: es como enseñarle a alguien a leer un idioma que no conoce. Primero separa las palabras (tokenización), luego cuenta cuáles se repiten (estadística) y, con suficiente práctica, entiende qué significan según el contexto (modelos semánticos).

### Aspectos Clave

1. **El pipeline típico de NLP:**
   ```
   Texto crudo → Normalización → Tokenización → Representación numérica → Modelo → Resultado
   ```
   - **Normalización:** minúsculas, quitar puntuación (con cuidado: "Mr Banks" no es lo mismo que "banks").
   - **Tokenización:** partir el texto en unidades (*tokens*): palabras, subpalabras o signos.
   - **Representación numérica:** conteos (bolsa de palabras, TF-IDF) o vectores semánticos (*embeddings*).
   - **Modelo:** un clasificador, un algoritmo de ranking o un LLM.

2. **Dos grandes enfoques:**

   | Enfoque | Cómo funciona | Ejemplos | Ventajas | Limitaciones |
   |---|---|---|---|---|
   | **Estadístico** | Cuenta frecuencias de palabras | TF-IDF, Naive Bayes, TextRank | Rápido, barato, explicable | No entiende sinónimos ni contexto |
   | **Semántico** | Representa palabras como vectores que capturan significado | Word2Vec, GloVe, Transformers (GPT) | Entiende contexto, sinónimos, ironía (a veces) | Más costoso, menos explicable |

   Los detalles de cada uno están en el [Módulo 3](../modulo3/tema1.md).

3. **Tareas de análisis de texto que pide el examen:**
   - **Extracción de palabras clave (key phrase extraction):** "El hotel tenía una alberca increíble pero el desayuno era caro" → `hotel`, `alberca increíble`, `desayuno`.
   - **Detección de entidades (NER):** identifica personas, lugares, organizaciones, fechas. "Ana viajó a Oaxaca en marzo" → Ana (Persona), Oaxaca (Ubicación), marzo (Fecha).
   - **Vinculación de entidades (entity linking):** desambigua una entidad y la liga a una referencia (por ejemplo, Wikipedia): ¿"Mercurio" es el planeta o el elemento?
   - **Análisis de sentimiento y minería de opiniones:** positivo, negativo, neutro o mixto; la minería de opiniones baja al nivel de aspecto ("alberca" positiva, "desayuno" negativo).
   - **Detección de idioma:** devuelve idioma, código ISO 639-1 (`es`, `en`) y una confianza de 0 a 1.
   - **Detección de PII:** encuentra datos personales (nombres, teléfonos, direcciones) y puede ocultarlos (*redactar*).
   - **Resumen:**
     - *Extractivo:* selecciona las oraciones más importantes del texto original.
     - *Abstractivo:* genera texto nuevo que resume las ideas (lo que hacen los LLMs).
   - **Traducción** y **clasificación** en categorías que tú defines.

4. **¿LLM o servicio especializado?**
   - Un **LLM** hace todo con un prompt y te deja combinar tareas ("traduce y resume esta reseña"), pero su salida varía entre llamadas.
   - **Azure Language en Foundry Tools** devuelve resultados **estructurados y deterministas**, ideales para *pipelines* automatizados.
   - Lo verás con código en la [Parte 2, Módulo 3](../../parte2/modulo3/tema1.md).

### Ejemplo mínimo en Python (sin nube)
```python
from collections import Counter
import re

texto = "La IA ayuda a las empresas. La IA mejora decisiones y la IA reduce costos."
stopwords = {"la", "las", "a", "y", "el", "los"}

tokens = re.findall(r"\w+", texto.lower())          # normalizar + tokenizar
tokens = [t for t in tokens if t not in stopwords]  # quitar stopwords
print(Counter(tokens).most_common(3))
# [('ia', 3), ('ayuda', 1), ('empresas', 1)]
```
- **Explicación:** con solo contar frecuencias ya sabemos que el texto trata de "IA". Así funciona el análisis estadístico más básico.

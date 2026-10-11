# Tema 1: Cuándo y cómo usar clasificación, detección, segmentación y análisis contextual de imágenes

### Descripción
Las cuatro tareas de visión son como **niveles de zoom** sobre la misma foto. Elegir la correcta depende de qué pregunta de negocio quieres responder y de cuánto detalle necesitas, porque más detalle implica más datos de entrenamiento, más cómputo y más costo.

Analogía con el súper:
- **Clasificación:** "¿Qué fruta pusiste en la báscula?" → "Manzana".
- **Detección:** "¿Qué hay en la banda de la caja y dónde está cada cosa?" → 3 cajas con etiqueta.
- **Segmentación:** "¿Exactamente qué píxeles son el plátano?" → contorno exacto.
- **Análisis contextual:** "¿Qué está pasando?" → "Un cliente pagando frutas en la caja".

### Aspectos Clave

1. **Clasificación de imágenes:**
   - **Qué devuelve:** una (o varias) etiquetas con probabilidad para **toda** la imagen.
   - **Cuándo usarla:** la imagen tiene un solo sujeto principal, o solo te importa la categoría general.
   - **Ejemplos:** identificar el tipo de fruta en una báscula; clasificar radiografías como normal/anormal; saber si una foto de producto cumple con las reglas del catálogo.
   - **Salida típica:**
     ```json
     { "predicciones": [ {"etiqueta": "manzana", "probabilidad": 0.94},
                         {"etiqueta": "naranja", "probabilidad": 0.05} ] }
     ```

2. **Detección de objetos:**
   - **Qué devuelve:** cada objeto con su clase, confianza y **bounding box** (x, y, ancho, alto).
   - **Cuándo usarla:** hay **varios objetos** y te importa **cuántos y dónde**.
   - **Ejemplos:** autocobro con varios productos; contar personas en un pasillo; detectar si un trabajador usa casco; huecos en anaqueles.
   - **Salida típica:**
     ```json
     { "objetos": [
         {"etiqueta": "manzana", "confianza": 0.91, "caja": {"x": 34, "y": 50, "w": 120, "h": 115}},
         {"etiqueta": "plátano", "confianza": 0.88, "caja": {"x": 210, "y": 40, "w": 180, "h": 90}} ] }
     ```

3. **Segmentación semántica:**
   - **Qué devuelve:** una **máscara**: cada píxel tiene asignada una clase.
   - **Cuándo usarla:** necesitas la **forma exacta**, medir áreas o separar objeto y fondo.
   - **Ejemplos:** medir el área de un tumor en imagen médica; autos autónomos que distinguen carretera, banqueta y peatón; quitar el fondo de una foto; agricultura (porcentaje de hoja con plaga).
   - **Variante:** la *segmentación de instancias* distingue también entre objetos de la misma clase (manzana 1, manzana 2).

4. **Análisis contextual de imágenes (multimodal):**
   - **Qué devuelve:** **lenguaje natural**: descripciones, etiquetas, respuestas a preguntas sobre la imagen.
   - **Cuándo usarla:** quieres entender relaciones y actividades, generar texto alternativo, o hacer preguntas abiertas ("¿hay algún riesgo de seguridad en esta foto?").
   - **Ejemplos:** *alt text* automático para accesibilidad; moderar fotos de usuarios; analizar capturas de pantalla, gráficas o diagramas; agentes que "ven".
   - **En Foundry:** modelos como GPT-4.1 o GPT-5.x con entrada de imagen ([Parte 2, Módulo 5](../../parte2/modulo5/tema2.md)).

### Tabla de decisión

| Necesito... | Tarea | Precisión de ubicación | Costo de etiquetar datos |
|---|---|---|---|
| Saber qué es | Clasificación | Ninguna | Bajo (una etiqueta por imagen) |
| Contar y ubicar objetos | Detección | Rectángulo | Medio (dibujar cajas) |
| Forma exacta / área | Segmentación | Píxel | Alto (pintar píxeles) |
| Describir o razonar sobre la escena | Multimodal | Semántica | Ninguno si usas un modelo preentrenado |

### Para el examen
- "Identificar la **ubicación** de cada vehículo en una imagen de tráfico" → **detección de objetos**.
- "Determinar si una foto contiene un perro o un gato" → **clasificación**.
- "Delimitar el contorno exacto de cada célula" → **segmentación**.
- "Generar una descripción para personas con discapacidad visual" → **análisis contextual / modelo multimodal**.

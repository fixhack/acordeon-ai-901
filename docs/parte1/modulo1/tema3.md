# Tema 3: IA, Machine Learning, Deep Learning, IA Generativa e IA Agéntica

### Descripción
Estos cinco términos se usan como sinónimos, pero son **capas que se contienen una dentro de otra**, como muñecas rusas (matrioskas). Entender la diferencia te ayuda a elegir la herramienta correcta y a no caer en las trampas del examen.

```
┌─────────────────────────────────────────────────────────┐
│ Inteligencia Artificial                                 │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Machine Learning                                  │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │ Deep Learning                               │  │  │
│  │  │  ┌───────────────────────────────────────┐  │  │  │
│  │  │  │ IA Generativa (LLMs, difusión)        │  │  │  │
│  │  │  │  ┌─────────────────────────────────┐  │  │  │  │
│  │  │  │  │ IA Agéntica (modelo + herram.)  │  │  │  │  │
│  │  │  │  └─────────────────────────────────┘  │  │  │  │
│  │  │  └───────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Aspectos Clave

1. **Inteligencia Artificial (IA):**
   - **Definición:** cualquier técnica que permite a una máquina imitar capacidades humanas (percibir, razonar, decidir, comunicarse). Incluye desde sistemas de reglas (*if/else*) de los años 80 hasta los LLMs actuales.
   - **Cuándo usarla:** es el paraguas; en la práctica eliges una de las subcategorías.

2. **Machine Learning (ML / aprendizaje automático):**
   - **Definición:** modelos que aprenden patrones a partir de datos en lugar de reglas explícitas.
   - **Tipos:**
     - **Supervisado:** con etiquetas. *Regresión* (predecir números) y *clasificación* (predecir categorías).
     - **No supervisado:** sin etiquetas. *Clustering* (agrupar por similitud).
     - **Por refuerzo:** un agente aprende por prueba y error con recompensas.
   - **Algoritmos típicos:** regresión lineal, árboles de decisión, random forest, k-means, Naive Bayes.
   - **Cuándo usarlo:** datos **tabulares** y estructurados (ventas, transacciones, sensores). Ejemplo: predecir la demanda de un producto o detectar fraude. Suele ser más barato, rápido y explicable que un LLM para estas tareas.

3. **Deep Learning (aprendizaje profundo):**
   - **Definición:** ML basado en **redes neuronales** con muchas capas que aprenden por sí solas las características relevantes.
   - **Arquitecturas clave:** CNN (imágenes), RNN/LSTM (secuencias, ya en desuso para texto) y **Transformers** (texto, imágenes, audio).
   - **Cuándo usarlo:** datos **no estructurados** (imágenes, audio, texto) y grandes volúmenes de datos. Ejemplo: reconocer productos en una foto o transcribir voz.

4. **IA Generativa:**
   - **Definición:** modelos de deep learning que **crean contenido nuevo** (texto, imágenes, video, audio, código) a partir de un *prompt*.
   - **Ejemplos:** LLMs (GPT, Claude, Mistral, Llama, Phi), modelos de difusión (GPT-Image, FLUX) y de video (Sora).
   - **Cuándo usarla:** redactar, resumir, traducir, conversar, generar código o imágenes; tareas abiertas donde hay muchas respuestas válidas.
   - **Cuándo NO:** cuando necesitas una respuesta exacta, determinista y auditable (un cálculo fiscal, una regla de negocio fija).

5. **IA Agéntica:**
   - **Definición:** sistemas que usan un modelo generativo como "cerebro" para **razonar, planear y actuar** usando herramientas, de forma (semi)autónoma.
   - **Componentes:** modelo + instrucciones + herramientas (+ conocimiento y memoria).
   - **Sistemas multiagente:** varios agentes especializados colaboran (uno investiga, otro analiza, otro ejecuta).
   - **Cuándo usarla:** procesos de varios pasos que requieren decidir qué hacer y tocar otros sistemas. Ejemplo: un agente que revisa una solicitud de reembolso, consulta la política, valida el ticket y crea la orden en el ERP.
   - **Cuándo NO:** si el flujo es siempre el mismo y predecible, un flujo de trabajo (*workflow*) tradicional es más barato, rápido y confiable.

### Tabla de decisión rápida

| Necesito... | Usa |
|---|---|
| Predecir ventas del próximo mes con datos históricos | Machine learning (regresión) |
| Segmentar clientes sin categorías previas | Machine learning (clustering) |
| Detectar defectos en fotos de una línea de producción | Deep learning (visión) |
| Responder preguntas de clientes en lenguaje natural | IA generativa |
| Detectar el idioma de miles de correos de forma consistente | Servicio especializado (Azure Language), no un LLM |
| Atender una solicitud completa: entender, consultar sistemas y ejecutar acciones | IA agéntica |

### Recursos
- [Ligera introducción a Deep Learning (acordeón AI-900)](https://github.com/josejesusguzman/acordeon-ia-900/blob/main/docs/intro_deep_learning.md)
- [Introducción a los conceptos de machine learning (Microsoft Learn)](https://learn.microsoft.com/es-es/training/modules/fundamentals-machine-learning/)

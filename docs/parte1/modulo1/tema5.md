# Tema 5: Bases técnicas de cómo funciona speech to text y text to speech

### Descripción
La IA de voz tiene dos direcciones:
- **Reconocimiento de voz (speech recognition / speech-to-text / STT):** audio → texto.
- **Síntesis de voz (speech synthesis / text-to-speech / TTS):** texto → audio.

Analogía: STT es un **taquígrafo** que escucha y escribe; TTS es un **locutor** que lee un guion en voz alta, cuidando entonación y pausas. Juntos permiten conversar con una máquina.

### Aspectos Clave

1. **Speech to text en 6 etapas:**

   | Etapa | Qué hace | Dato clave |
   |---|---|---|
   | 1. Captura de audio | El micrófono convierte la onda en señal digital muestreándola | 16 kHz para voz (8–16 kHz); 44.1 kHz para música |
   | 2. Preprocesamiento | Extrae características compactas (MFCC) | Ventanas de 20–30 ms, ~13 coeficientes por ventana |
   | 3. Modelo acústico | Predice **fonemas** a partir de las características | El inglés tiene ~44 fonemas; hoy se usan Transformers |
   | 4. Modelo de lenguaje | Decide qué palabras tienen sentido | "there" vs "their" suenan igual; el contexto decide |
   | 5. Decodificación | Busca la mejor secuencia de palabras | *Beam search* |
   | 6. Posprocesamiento | Mayúsculas, puntuación, números ("tres p m" → "3 PM") | Devuelve marcas de tiempo y confianza por palabra |

2. **Text to speech en 4 etapas:**

   | Etapa | Qué hace | Ejemplo |
   |---|---|---|
   | 1. Normalización de texto | Expande abreviaturas, números y símbolos | "Dr. López pagó $25.50" → "Doctor López pagó veinticinco pesos con cincuenta centavos" |
   | 2. Análisis lingüístico | Convierte grafemas en fonemas (G2P) | "read" se pronuncia distinto en presente y pasado |
   | 3. Generación de prosodia | Decide ritmo, tono, énfasis y pausas | Las preguntas suben de tono al final |
   | 4. Síntesis de onda | Un **vocoder neuronal** genera el audio | WaveNet, HiFi-GAN; 16,000–48,000 muestras por segundo |

3. **Escenarios típicos:**
   - **STT:** transcripción de llamadas de servicio al cliente, subtítulos en tiempo real, dictado médico, minutas de reuniones, asistentes de voz.
   - **TTS:** chatbots con voz, lectura en voz alta para accesibilidad, notificaciones (GPS), cursos narrados, prototipos de audiolibros.
   - **Combinados:** IVR (menús telefónicos por voz), agentes de voz en tiempo real, aprendizaje de idiomas.

4. **Consideraciones antes de implementar:**
   - **Calidad de audio:** ruido, micrófono y distancia afectan directamente la precisión.
   - **Idiomas y dialectos:** confirma que el español de México (`es-MX`) u otra variante esté soportada.
   - **Privacidad:** el audio puede contener datos sensibles.
   - **Latencia:** una conversación necesita respuesta en tiempo real; una transcripción por lotes puede esperar.
   - **Accesibilidad:** ofrece siempre una alternativa de texto (principio de *inclusión*).

### Para el examen
- "Convertir grabaciones de llamadas a texto para analizarlas" → **speech recognition**.
- "Leer en voz alta las respuestas del chatbot" → **speech synthesis**.
- "Un asistente con el que hablas y te responde hablando" → ambos (en Foundry: **Voice Live**).

Profundizas en el [Módulo 4](../modulo4/tema1.md) y lo programas en la [Parte 2, Módulo 4](../../parte2/modulo4/tema1.md).

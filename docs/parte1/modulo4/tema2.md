# Tema 2: Diferencia técnica entre speech to text y text to speech

### Descripción
Aunque suelen mencionarse juntos, el reconocimiento (STT) y la síntesis (TTS) son **problemas inversos** con retos distintos. STT tiene que **reducir** una señal enorme y ruidosa a unas cuantas palabras; TTS tiene que **expandir** unas cuantas palabras a una señal rica y natural. Microsoft Learn lo resume así: el vocoder hace lo inverso al reconocimiento de voz.

Analogía: STT es como escuchar una canción y escribir la letra; TTS es como leer la letra y cantarla con la entonación correcta.

### Aspectos Clave

1. **Comparación lado a lado:**

   | Aspecto | Speech to text (reconocimiento) | Text to speech (síntesis) |
   |---|---|---|
   | Entrada | Audio (onda) | Texto |
   | Salida | Texto + marcas de tiempo + confianza | Audio (onda) |
   | Representación intermedia | MFCC / espectrograma → fonemas | Fonemas + prosodia → espectrograma Mel |
   | Modelos clave | Modelo acústico + modelo de lenguaje | Modelo acústico + **vocoder neuronal** |
   | Problema central | **Ambigüedad**: "hay", "ahí", "ay" suenan igual | **Naturalidad**: entonación, ritmo, emoción |
   | Normalización | *Inversa*: "tres p m" → "3 PM" | *Directa*: "3 PM" → "tres p m" |
   | Algoritmo de búsqueda | *Beam search* sobre hipótesis de palabras | No hay búsqueda; se genera la onda |
   | Fuente típica de error | Ruido, acentos, vocabulario técnico | Prosodia plana (voz robótica), homógrafos |
   | Personalización | Modelos de lenguaje con vocabulario del dominio (médico, legal) | Voces personalizadas, estilos, SSML |

2. **Pipeline STT:**
   ```
   🎤 Audio → Muestreo (16 kHz) → MFCC → Modelo acústico (fonemas) → Modelo de lenguaje → Beam search → Posprocesamiento → "Envía el reporte el viernes."
   ```
   - El **modelo acústico** dice qué sonidos escuchó: /e/ /n/ /b/ /i/ /a/...
   - El **modelo de lenguaje** decide qué palabras tienen sentido: "envía el reporte" y no "en vía el re porte".
   - El **decodificador** combina ambos y elige la transcripción más probable.

3. **Pipeline TTS:**
   ```
   "Dr. Chen, su cita es a las 3:00 PM" → Normalización → G2P (fonemas) → Prosodia → Espectrograma Mel → Vocoder → 🔊
   ```
   - **G2P:** "though", "through" y "cough" comparten "ough" y se pronuncian distinto; el modelo usa contexto.
   - **Prosodia:** el énfasis cambia el significado: "*Yo* nunca dije que él se comió el pastel" vs. "Yo nunca dije que él se comió el *pastel*".
   - **Vocoder:** WaveNet, WaveGlow o HiFi-GAN generan entre 16,000 y 48,000 muestras por segundo.

4. **Métricas para evaluarlos:**
   - **STT → WER (Word Error Rate):** `(sustituciones + eliminaciones + inserciones) / palabras de referencia`. Menor es mejor.
   - **TTS → MOS (Mean Opinion Score):** personas califican la naturalidad de 1 a 5. Mayor es mejor.
   ```python
   # pip install jiwer
   from jiwer import wer

   referencia = "envía el reporte el viernes por la tarde"
   transcripcion = "envía el reporte del viernes por la tarde"
   print(f"WER: {wer(referencia, transcripcion):.2%}")   # 1 sustitución en 8 palabras = 12.50%
   ```

5. **Cómo se ven en Azure Speech (Parte 2):**

   | | STT | TTS |
   |---|---|---|
   | Clase principal | `SpeechRecognizer` | `SpeechSynthesizer` |
   | Configuración de audio | `AudioConfig` (micrófono, archivo) | `AudioOutputConfig` (bocina, archivo) |
   | Método | `recognize_once_async()` / `start_continuous_recognition()` | `speak_text_async()` / `speak_ssml_async()` |
   | Modos | Tiempo real o **batch** (lotes) | Tiempo real o generación de archivos |

### Para el examen
Si la pregunta menciona **fonemas → palabras**, **ruido** o **transcripción**, es reconocimiento. Si menciona **voz neuronal**, **tono**, **velocidad**, **prosodia** o **SSML**, es síntesis.

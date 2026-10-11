# Tema 1: Captura de audio — Convertir audio analógico en digital (fundamentos técnicos desde el espectrograma)

### Descripción
El sonido es una **onda continua** de presión en el aire. Una computadora solo maneja números discretos, así que el primer paso de cualquier sistema de voz es convertir esa onda analógica en una secuencia de números (digitalizarla) y luego transformarla en una representación que el modelo pueda "ver": el **espectrograma**.

Analogía: grabar audio es como filmar una pelota en movimiento con una cámara de fotos en ráfaga. Cada foto es una **muestra**. Si tomas pocas fotos por segundo, te pierdes movimientos rápidos (sonidos agudos); si tomas muchas, el archivo es enorme.

Lectura oficial: [Reconocimiento de voz – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/introduction-ai-speech/3-speech-recognition?pivots=text)

### Aspectos Clave

1. **Muestreo (sampling):**
   - El micrófono convierte la presión del aire en voltaje y un convertidor analógico-digital (ADC) **mide** ese voltaje miles de veces por segundo.
   - **Frecuencia de muestreo:**
     - **8 kHz:** telefonía.
     - **16 kHz:** estándar para reconocimiento de voz (equilibrio entre claridad y procesamiento).
     - **44.1 kHz:** música (calidad CD).
   - **Teorema de Nyquist:** para capturar una frecuencia `f` necesitas muestrear al menos a `2f`. Con 16 kHz capturas hasta 8 kHz, suficiente para la voz humana.

2. **Cuantización (profundidad de bits):**
   - Cada muestra se guarda como un número entero. Con **16 bits** hay 65,536 niveles posibles de amplitud (formato **PCM16**, el que usa Azure Speech y Voice Live).
   - Un segundo de audio a 16 kHz y 16 bits mono ocupa 16,000 × 2 bytes = **32 KB**.

3. **Forma de onda (waveform):**
   Es la gráfica de amplitud contra tiempo. Muestra **cuándo** hay sonido y qué tan fuerte, pero no **qué frecuencias** lo componen, y las frecuencias son las que distinguen una "a" de una "e".

4. **Del tiempo a la frecuencia: transformada de Fourier**
   - Cualquier sonido complejo es la suma de ondas simples de distintas frecuencias.
   - La **transformada de Fourier** descompone una ventana de audio en esas frecuencias.
   - Se aplica a **ventanas cortas de 20–30 ms** (en ese lapso la voz es casi estable) que se traslapan.

5. **Espectrograma:**
   - Apila los resultados de Fourier de cada ventana: **eje X = tiempo**, **eje Y = frecuencia**, **color = energía**.
   - Es literalmente una **imagen del sonido**; por eso técnicas de visión y Transformers funcionan tan bien con audio.
   - **Espectrograma Mel:** reescala las frecuencias a la **escala Mel**, que imita al oído humano (distinguimos mejor tonos graves que agudos).

6. **MFCC (Mel-Frequency Cepstral Coefficients):**
   1. Dividir el audio en ventanas de 20–30 ms.
   2. Aplicar transformada de Fourier.
   3. Mapear a la escala Mel.
   4. Extraer ~**13 coeficientes** por ventana que resumen la forma del espectro.
   ```
   Ventana 1: [-113.2, 45.3, 12.1, -3.4, 7.8, ...]   # 13 coeficientes
   Ventana 2: [-112.8, 44.7, 11.8, -3.1, 7.5, ...]
   ```
   Esta secuencia de vectores es la entrada del **modelo acústico**.

### Práctica en Python
```python
# pip install librosa matplotlib
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Carga un audio de ejemplo y lo re-muestrea a 16 kHz
audio, sr = librosa.load(librosa.ex("libri1"), sr=16000)
print(f"Muestras: {len(audio)}  |  Duración: {len(audio)/sr:.1f} s  |  Frecuencia: {sr} Hz")

# 1) Espectrograma Mel (ventanas de 25 ms con salto de 10 ms)
mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=400, hop_length=160, n_mels=80)
mel_db = librosa.power_to_db(mel, ref=np.max)

# 2) MFCC: 13 coeficientes por ventana
mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13, n_fft=400, hop_length=160)
print(f"Forma de los MFCC: {mfcc.shape}  (13 coeficientes x número de ventanas)")

fig, ax = plt.subplots(3, 1, figsize=(10, 8))
librosa.display.waveshow(audio, sr=sr, ax=ax[0]); ax[0].set_title("Forma de onda")
librosa.display.specshow(mel_db, sr=sr, hop_length=160, x_axis="time", y_axis="mel", ax=ax[1]); ax[1].set_title("Espectrograma Mel")
librosa.display.specshow(mfcc, sr=sr, hop_length=160, x_axis="time", ax=ax[2]); ax[2].set_title("MFCC")
plt.tight_layout(); plt.show()
```
- **Explicación:**
  - `n_fft=400` a 16 kHz = ventanas de 25 ms; `hop_length=160` = saltos de 10 ms (ventanas traslapadas).
  - `librosa.ex("libri1")` descarga un audio de ejemplo; puedes cambiarlo por la ruta de tu propio `.wav`.
  - Verás que la forma de onda solo muestra volumen, mientras el espectrograma revela la estructura de la voz.

### Factores que afectan la precisión
Ruido de fondo, calidad del micrófono, distancia de quien habla, eco y compresión del audio. Si una transcripción sale mal, muchas veces el problema empezó aquí.

### Recursos
- [Understanding the Mel Spectrogram](https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53)
- [But what is the Fourier Transform? – 3Blue1Brown](https://www.youtube.com/watch?v=spUNpyF58BY)

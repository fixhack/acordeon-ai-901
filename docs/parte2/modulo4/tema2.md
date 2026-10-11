# Tema 2: Explicación de los SDK de voz y Voice Live de Microsoft Foundry con Python

### Descripción
En Foundry tienes dos caminos para dar voz a tus aplicaciones:
1. **Speech SDK** (`azure-cognitiveservices-speech`): piezas separadas de STT y TTS. Tú controlas cada paso y conectas la lógica en medio.
2. **Voice Live API** (`azure-ai-voicelive`): un servicio **voz a voz (speech-to-speech)** totalmente administrado que integra reconocimiento, un modelo generativo y síntesis en una sola conexión en tiempo real, con manejo de interrupciones.

Analogía: el Speech SDK es armar tu propio equipo de sonido por componentes (micrófono, mezcladora, bocinas). Voice Live es una bocina inteligente que ya trae todo integrado: solo la conectas.

### Aspectos Clave

1. **Text to speech con el Speech SDK:**
   ```python
   import os
   from dotenv import load_dotenv
   import azure.cognitiveservices.speech as speechsdk

   load_dotenv()
   speech_config = speechsdk.SpeechConfig(subscription=os.getenv("FOUNDRY_KEY"), endpoint=os.getenv("ENDPOINT"))

   # Voz neuronal en español de México (prueba también "es-MX-JorgeNeural")
   speech_config.speech_synthesis_voice_name = "es-MX-DaliaNeural"

   # Salida: bocinas. Para guardar a archivo: AudioOutputConfig(filename="saludo.wav")
   audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
   synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

   resultado = synthesizer.speak_text_async("¡Hola! Bienvenido al acordeón de la AI-901.").get()

   if resultado.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
       print("Audio generado")
   elif resultado.reason == speechsdk.ResultReason.Canceled:
       detalles = resultado.cancellation_details
       print(f"Cancelado: {detalles.reason} {detalles.error_details}")
   ```
   - **Explicación:**
     - `speech_synthesis_voice_name` elige la voz. Microsoft Learn usa `en-US-Ava:DragonHDLatestNeural`, una voz **multilingüe HD** que habla distintos idiomas según el texto.
     - `AudioOutputConfig` define a dónde va el audio: bocina o archivo.
     - `speak_text_async(...).get()` sintetiza y espera el resultado.

2. **Controlar la voz con SSML:**
   SSML (*Speech Synthesis Markup Language*) es XML para controlar velocidad, tono, pausas, énfasis y pronunciación.
   ```python
   ssml = """
   <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-MX">
     <voice name="es-MX-DaliaNeural">
       Tu vuelo a Cancún sale a las <say-as interpret-as="time" format="hms12">7:45pm</say-as>.
       <break time="500ms"/>
       <prosody rate="-15%" pitch="+5%">Te recomendamos llegar dos horas antes.</prosody>
     </voice>
   </speak>
   """
   resultado = synthesizer.speak_ssml_async(ssml).get()
   ```
   - **Explicación:** `<break>` agrega pausas, `<prosody>` ajusta velocidad y tono, `<say-as>` controla cómo se leen horas, fechas o números. Es la forma de evitar la "voz robótica" (prosodia plana).

3. **Voice Live: arquitectura**
   ```
   🎤 Audio del usuario ──WebSocket──► Voice Live ──► [STT] → [Modelo generativo / Agente] → [TTS] ──► 🔊
                                           ▲                                                     │
                                           └────── detección de turnos e interrupciones ◄────────┘
   ```
   - **Servicio administrado:** no montas ni mantienes el backend.
   - Usa el **modelo generativo que elijas** junto con sus propios modelos acústicos.
   - **Detección de voz (VAD) y de fin de turno**, **cancelación de eco** e **interrupciones** (*barge-in*): si hablas mientras el agente habla, se calla y te escucha.
   - Configurable en el Playground: voz, instrucciones, **participación proactiva** (el agente puede iniciar).
   - **Voice mode** integra Voice Live dentro de un **agente de Foundry**, así la configuración de voz vive en el agente y tu cliente es más sencillo.

4. **Voice Live con Python (SDK asíncrono):**
   ```python
   # pip install "azure-ai-voicelive[aiohttp]" azure-identity python-dotenv pyaudio
   import asyncio, os
   from dotenv import load_dotenv
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.voicelive.aio import connect
   from azure.ai.voicelive.models import (
       RequestSession, Modality, InputAudioFormat, OutputAudioFormat,
       ServerVad, AzureStandardVoice, ServerEventType,
   )

   load_dotenv()

   async def main():
       async with connect(
           endpoint=os.environ["AZURE_VOICELIVE_ENDPOINT"],
           credential=AzureKeyCredential(os.environ["AZURE_VOICELIVE_API_KEY"]),
           model="gpt-realtime",                     # modelo que razona en la conversación
       ) as conexion:
           # 1) Configurar la sesión: instrucciones, voz, formatos y detección de turnos
           await conexion.session.update(session=RequestSession(
               modalities=[Modality.TEXT, Modality.AUDIO],
               instructions="Eres un asistente de viajes amable. Responde en español de México, breve.",
               voice=AzureStandardVoice(name="es-MX-DaliaNeural", type="azure-standard"),
               input_audio_format=InputAudioFormat.PCM16,
               output_audio_format=OutputAudioFormat.PCM16,
               turn_detection=ServerVad(threshold=0.5, prefix_padding_ms=300, silence_duration_ms=500),
           ))

           # 2) Procesar los eventos que manda el servidor
           async for evento in conexion:
               if evento.type == ServerEventType.SESSION_UPDATED:
                   print("Sesión lista: empieza a enviar audio del micrófono")
               elif evento.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                   print("El usuario empezó a hablar → detener reproducción (interrupción)")
               elif evento.type == ServerEventType.RESPONSE_AUDIO_DELTA:
                   audio_pcm = evento.delta              # fragmento de audio para reproducir
               elif evento.type == ServerEventType.ERROR:
                   print("Error:", evento.error.message)

   asyncio.run(main())
   ```
   - **Explicación:**
     - El SDK es **solo asíncrono** (`async/await`) y mantiene una **conexión WebSocket** abierta.
     - `session.update` configura instrucciones, **voz** (puede ser una voz neuronal de Azure o una de OpenAI como `alloy`), formatos **PCM16** y **ServerVad** (el servidor detecta cuándo empiezas y terminas de hablar).
     - Todo es **orientado a eventos**: `RESPONSE_AUDIO_DELTA` trae trozos de audio para reproducir; `INPUT_AUDIO_BUFFER_SPEECH_STARTED` indica que el usuario interrumpió.
     - Este esqueleto no incluye la captura del micrófono ni la reproducción. El portal de Foundry genera un **ejemplo completo** (con PyAudio) que maneja sesión, dispositivos de audio, streams e interrupciones: cópialo desde el Playground de Voice Live.

5. **¿Speech SDK o Voice Live?**

   | Necesidad | Usa |
   |---|---|
   | Transcribir audio o generar archivos de voz | Speech SDK |
   | Control total de cada etapa (ej. traducir en medio, guardar transcripción) | Speech SDK + tu lógica |
   | Conversación natural en tiempo real, con interrupciones | **Voice Live** |
   | Que un agente de Foundry existente "hable" | **Voice mode** del agente (Voice Live) |
   | Responder a prompts hablados con un modelo multimodal (habilidad del examen) | Modelo con entrada de audio o Voice Live |

### Recursos
- [Galería de voces de Azure Speech](https://speech.microsoft.com/portal/voicegallery)
- [Referencia de SSML](https://learn.microsoft.com/es-es/azure/ai-services/speech-service/speech-synthesis-markup)
- [Voice Live API](https://learn.microsoft.com/es-es/azure/ai-services/speech-service/voice-live)
- [Paquete azure-ai-voicelive en PyPI](https://pypi.org/project/azure-ai-voicelive/)

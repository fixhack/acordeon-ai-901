# Tema 4: Tips de generación de videos con Microsoft Foundry

### Descripción
Microsoft Foundry ofrece **Sora** y **Sora 2** de OpenAI, los únicos modelos **nativos de generación de video** del catálogo (otros modelos son multimodales pero no generan video). Generar video es costoso y **asíncrono**: creas un trabajo, esperas de 1 a 5 minutos y descargas el resultado.

Analogía: pedir un video a Sora es como encargar un pastel: das las instrucciones (prompt), te dan un número de pedido (ID del job), preguntas de vez en cuando si ya está listo (polling) y cuando dice "completado" lo recoges (descarga).

### Aspectos Clave

1. **Sora vs. Sora 2:**

   | | Sora | Sora 2 (preview) |
   |---|---|---|
   | Texto a video | ✅ | ✅ |
   | Imagen a video | ✅ (acepta imagen de entrada) | ✅ |
   | Video a video (**remix**) | ❌ | ✅ ediciones dirigidas sin regenerar todo |
   | **Audio** generado | ❌ | ✅ |
   | Acceso | Azure OpenAI / Video Playground | **API v1** de Azure OpenAI / Video Playground |

2. **Flujo asíncrono con REST:**
   ```bash
   # 1) Crear el trabajo -> devuelve un video_id
   curl -X POST "https://<recurso>.openai.azure.com/openai/v1/videos" \
     -H "Content-Type: application/json" \
     -H "api-key: $AZURE_OPENAI_API_KEY" \
     -d '{"model": "sora-2",
          "prompt": "Primer plano cinematográfico de gotas de lluvia resbalando por una ventana con luces de neón de noche.",
          "size": "1280x720",
          "seconds": "8"}'

   # 2) Consultar el estado hasta que sea "completed" (o "failed")
   curl "https://<recurso>.openai.azure.com/openai/v1/videos/{video_id}" -H "api-key: $AZURE_OPENAI_API_KEY"

   # 3) Descargar (solo cuando el estado es "completed")
   curl -L "https://<recurso>.openai.azure.com/openai/v1/videos/{video_id}/content?variant=video" \
     -H "api-key: $AZURE_OPENAI_API_KEY" --output video.mp4
   ```

3. **El mismo flujo en Python:**
   ```python
   import os, time
   from dotenv import load_dotenv
   from openai import OpenAI

   load_dotenv()
   client = OpenAI(base_url=os.environ["ENDPOINT"], api_key=os.environ["FOUNDRY_KEY"])

   video = client.videos.create(
       model="sora-2",                    # nombre de tu deployment
       prompt=("Un trajinero navega por los canales de Xochimilco al amanecer, neblina ligera, "
               "cámara en dron que avanza lentamente, estilo documental, sonido de agua y aves."),
       size="1280x720",
       seconds="8",
   )
   print("Job creado:", video.id)

   while video.status not in ("completed", "failed"):
       time.sleep(15)                     # consulta cada 15 s (tarda 1-5 min)
       video = client.videos.retrieve(video.id)
       print("Estado:", video.status)

   if video.status == "completed":
       contenido = client.videos.download_content(video.id, variant="video")
       contenido.write_to_file("xochimilco.mp4")
       print("Guardado: xochimilco.mp4")
   ```
   - **Explicación:** misma lógica que REST: **crear → consultar (polling) → descargar**. Necesitas una versión reciente del paquete `openai` que incluya `client.videos`; si tu versión no lo tiene, usa los comandos REST de arriba.

4. **Tips para escribir prompts de video:**
   - **Estructura recomendada:** *sujeto + acción + escenario + estilo visual + cámara + iluminación + (audio en Sora 2)*.
     - ❌ "Un perro en la playa."
     - ✅ "Un xoloitzcuintle corre por la orilla de una playa en Oaxaca al atardecer, cámara lenta en *travelling* lateral, luz dorada, estilo comercial, se escuchan olas."
   - **Describe el movimiento de cámara:** plano fijo, paneo, *dolly in*, dron, cámara en mano.
   - **Una acción principal por clip:** los videos cortos funcionan mejor con una sola idea clara.
   - **Especifica la física y el tiempo:** "camina con las patas sobre la arena", "la vela se consume lentamente".
   - **Estilo consistente:** "estilo stop-motion", "animación 3D tipo plastilina", "documental".
   - **Empieza con clips cortos y baja resolución** para iterar rápido y barato; sube calidad al final.
   - **Usa imagen de referencia** para controlar el primer cuadro (personaje, producto, encuadre).
   - **Remix (Sora 2)** para ajustes puntuales en lugar de regenerar todo.

5. **Costos y operación:**
   - Generar video consume muchos recursos: más segundos y más resolución = más costo y más espera.
   - Implementa **reintentos** y **timeouts**; los jobs pueden fallar.
   - Guarda el `video_id`: el video solo se descarga cuando el estado es `completed`.

6. **IA responsable:**
   - Restricciones sobre **personas reales**, **personajes con derechos de autor** y ciertos tipos de contenido.
   - Etiqueta el contenido generado (**transparencia**); los videos realistas pueden usarse para desinformar.
   - Revisa el video antes de publicarlo: los modelos pueden producir errores físicos o sesgos.

### Usos típicos
Storyboards y videos conceptuales, animaciones cortas, videos de marketing, previsualizaciones cinematográficas y material educativo.

### Recursos
- [Generación de video con Sora en Microsoft Foundry](https://learn.microsoft.com/es-es/azure/foundry/openai/concepts/video-generation)

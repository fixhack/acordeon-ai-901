# Tema 3: Así funciona Alexa internamente

### Descripción
Alexa (y en general cualquier asistente de voz: Siri, Google Assistant o un agente de voz hecho con Foundry) es el ejemplo perfecto de cómo se **encadenan** todas las piezas de IA de voz: detección de palabra de activación, reconocimiento, comprensión, razonamiento/acción y síntesis. Entender este flujo te ayuda a diseñar tus propios agentes de voz.

> [!NOTE]
> Amazon no publica todos los detalles internos de Alexa. Esta es la arquitectura general documentada por Amazon para desarrolladores (Alexa Skills Kit) y la que siguen los asistentes de voz modernos.

Analogía: es como un restaurante. El mesero (bocina) solo pone atención cuando dices "¡joven!" (*wake word*), anota tu pedido (STT), la cocina entiende qué quieres (NLU), prepara el platillo (skill / herramienta) y el mesero te lo entrega con una sonrisa (TTS).

### Aspectos Clave

1. **Detección de la palabra de activación (wake word) — en el dispositivo:**
   - Un modelo **pequeño y de bajo consumo** escucha continuamente **dentro del dispositivo** buscando "Alexa".
   - Nada se envía a la nube hasta que detecta la palabra (por privacidad, latencia y costo). El anillo de luz indica que empezó a transmitir.
   - Técnicas de apoyo: arreglo de micrófonos con *beamforming* (enfoca la voz de quien habla) y cancelación de eco (para oírte aunque esté sonando música).

2. **Reconocimiento automático de voz (ASR) — en la nube:**
   - El audio se transmite (*streaming*) a la nube.
   - Pasa por el pipeline que ya conoces: características → modelo acústico → modelo de lenguaje → decodificación.
   - Resultado: "pon música de café tacvba en la sala".

3. **Comprensión del lenguaje natural (NLU):**
   - Convierte el texto en una estructura que un programa entiende:
     - **Intención (intent):** `PlayMusic`
     - **Ranuras / entidades (slots):** `artista = Café Tacvba`, `dispositivo = sala`
   - Este es el mismo concepto que el *Conversational Language Understanding* de Azure Language.

4. **Enrutamiento y ejecución (skills / herramientas):**
   - El intent se envía a la **skill** correspondiente (música, clima, domótica, una skill de un tercero).
   - La skill llama APIs externas (Spotify, el foco inteligente, el servicio del clima) y arma una respuesta.
   - En términos de agentes: **las skills son herramientas** y el enrutador es el **orquestador**.

5. **Generación de la respuesta y síntesis de voz (TTS):**
   - Se genera el texto de respuesta (a menudo en SSML para controlar pausas y entonación).
   - Un modelo de **TTS neuronal** produce el audio que se transmite de regreso a la bocina.

6. **La evolución: de intents a LLMs (Alexa+)**
   - El modelo clásico (intents + slots) es preciso pero rígido: si dices algo fuera de lo previsto, falla.
   - En 2025 Amazon presentó **Alexa+**, que usa **modelos de lenguaje grandes** para conversar con más naturalidad, mantener contexto y orquestar acciones con herramientas, es decir, se volvió un **agente**.

### El mismo flujo con Microsoft Foundry

| Etapa de Alexa | Equivalente en Foundry |
|---|---|
| Wake word en dispositivo | Keyword recognition del Speech SDK |
| ASR | Azure Speech – Speech to text |
| NLU (intents y slots) | LLM del agente (o Azure Language CLU) |
| Skills | **Tools** del agente (MCP, OpenAPI, funciones) |
| TTS | Azure Speech – Text to speech (voces neuronales) |
| Todo integrado en tiempo real | **Voice Live API** (speech-to-speech con interrupciones) |

```
🎤 "Alexa..." → [Wake word local] → ☁️ [STT] → [NLU / LLM] → [Skill / Tool] → [TTS] → 🔊
                                       ↑______________ Voice Live integra este tramo ______________↑
```

### Para reflexionar (IA responsable)
- **Privacidad:** el dispositivo escucha siempre; por eso la detección es local y hay botón para silenciar micrófonos.
- **Transparencia:** el usuario debe saber cuándo está grabando (luz) y poder borrar sus grabaciones.
- **Inclusión:** acentos, dialectos y personas con dificultades del habla deben poder usarlo.

### Recursos
- [Alexa Skills Kit: conceptos de interaction model (intents, slots)](https://developer.amazon.com/en-US/docs/alexa/ask-overviews/what-is-the-alexa-skills-kit.html)
- [Voice Live API en Microsoft Foundry](https://learn.microsoft.com/es-es/azure/ai-services/speech-service/voice-live)

# Tema 3: Tutorial — Mi primer agente en Microsoft Foundry

**Objetivo:** Crear un agente en el portal de Microsoft Foundry, darle instrucciones, conocimiento y una herramienta, y probarlo en el Playground sin escribir código.

> [!NOTE]
> El portal de Foundry cambia seguido. Si un botón no está exactamente donde dice este tutorial, busca la opción equivalente (por ejemplo **Build** → **Agents**). Las prácticas de Microsoft Learn están en inglés; puedes traducirlas con el navegador.

## Paso a Paso:

1. **Crear el proyecto de Foundry:**
   - Entra a [https://ai.azure.com](https://ai.azure.com) con tu cuenta de Azure.
   - Selecciona **Create project** (Crear proyecto). Escribe un nombre (por ejemplo `acordeon-ai901`).
   - En opciones avanzadas elige suscripción, grupo de recursos y región. Foundry crea un **recurso de Foundry** y, dentro de él, tu **proyecto**.

2. **Desplegar un modelo:**
   - Ve a **Build → Models** (o al catálogo de modelos) y busca `gpt-4.1-mini`.
   - Selecciona **Deploy** con la configuración por defecto (tipo *Global Standard*).
   - Anota el **nombre del deployment**; lo usarás en el código.

3. **Crear el agente:**
   - Ve a **Build → Agents** y selecciona **Create agent**.
   - Ponle nombre: `agente-viajes`.
   - Elige el deployment `gpt-4.1-mini`.
   - En **Instructions** pega:
     ```text
     Eres "Viajero", un asistente de viajes por México.
     - Respondes en español de México con un tono cercano.
     - Das máximo 5 recomendaciones en viñetas.
     - Si te preguntan por políticas de la agencia, usa SOLO los archivos de conocimiento
       y cita el documento. Si no está, di que no tienes ese dato.
     ```

4. **Agregar conocimiento (knowledge):**
   - Crea en tu computadora un archivo `politicas.txt` con:
     ```text
     Política de cancelación de Contoso Travel
     - Cancelaciones con más de 7 días de anticipación: reembolso del 100%.
     - Entre 2 y 7 días: reembolso del 50%.
     - Menos de 48 horas: sin reembolso.
     ```
   - En el agente, en **Knowledge**, agrega el archivo (opción de cargar archivos / File search).
   - Foundry divide el archivo en fragmentos, genera embeddings y crea un índice vectorial automáticamente.

5. **Agregar una herramienta (tool):**
   - En **Tools**, agrega **Code Interpreter** (permite que el agente escriba y ejecute Python para cálculos o gráficas).

6. **Probar en el Playground:**
   - Prueba estos prompts y observa las diferencias:

     | Prompt | Qué deberías ver |
     |---|---|
     | `Recomiéndame 3 lugares para comer en Puebla` | Respuesta del modelo (conocimiento general) |
     | `Si cancelo 5 días antes, ¿cuánto me reembolsan?` | 50% con **cita** a `politicas.txt` (RAG) |
     | `Un vuelo cuesta 3,450 y el hotel 1,280 por noche, 3 noches. ¿Total con 16% de IVA?` | El agente usa **Code Interpreter** para calcular |
     | `¿Cuál es la política de mascotas?` | "No tengo ese dato" (no inventa) |

7. **Ver el código:**
   - Selecciona **View code** (Ver código) en el Playground. Foundry te muestra el código Python que llama al agente usando el **SDK de Foundry** y la **Responses API**. Lo usarás en la [Parte 2, Módulo 1](../../parte2/modulo1/tema4.md).

## Qué aprendiste
- Un agente = **modelo + instrucciones + herramientas + conocimiento**.
- **Tools = acciones**, **Knowledge = contexto**.
- El Playground es el lugar para validar prompts y comportamiento antes de escribir código.

## Práctica oficial de Microsoft Learn
- [Ejercicio: Explorar la IA generativa](https://learn.microsoft.com/es-es/training/modules/fundamentals-generative-ai/7a-exercise)
- [Ejercicio: Introducción a la IA generativa y los agentes en Microsoft Foundry](https://learn.microsoft.com/es-es/training/modules/get-started-with-generative-ai-and-agents/6-exercise)

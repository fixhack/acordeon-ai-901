# Tema 2: Cuándo usar system prompt, cuándo usar RAG y cuándo usar fine-tuning

### Descripción
Hay tres palancas para adaptar un modelo a tu caso de uso, y elegir la incorrecta sale caro:
- **System prompt (ingeniería de prompts):** le dices al modelo **cómo comportarse**.
- **RAG:** le das al modelo **información** que no tiene, en el momento de la pregunta.
- **Fine-tuning:** **reentrenas** parcialmente el modelo con ejemplos para cambiar su comportamiento de forma permanente.

Analogía: preparar a un nuevo empleado.
- **System prompt** = darle un **instructivo** el primer día ("sé amable, responde en viñetas").
- **RAG** = darle acceso a la **biblioteca de manuales** para que consulte cuando lo necesite.
- **Fine-tuning** = mandarlo a un **curso intensivo** hasta que el estilo y las habilidades se le vuelvan naturales.

### Aspectos Clave

1. **Comparación:**

   | | System prompt | RAG | Fine-tuning |
   |---|---|---|---|
   | Cambia... | Comportamiento, tono, formato, reglas | **Conocimiento** disponible en cada respuesta | **Comportamiento aprendido** (pesos del modelo) |
   | ¿Modifica el modelo? | No | No | **Sí** |
   | Datos necesarios | Ninguno (unos ejemplos) | Tus documentos | Cientos a miles de pares prompt–respuesta de alta calidad |
   | Información actualizada | No aplica | ✅ Actualizas el índice y listo | ❌ Hay que reentrenar |
   | Citas / trazabilidad | No | ✅ | No |
   | Costo inicial | Mínimo | Medio (indexar) | Alto (entrenar + **hospedar** el modelo ajustado) |
   | Tiempo para implementar | Minutos | Horas/días | Días/semanas |
   | Riesgo principal | Prompts largos y frágiles | Mala recuperación | Sobreajuste, mantenimiento, costo |

2. **Usa system prompt cuando:**
   - Quieres definir **rol, tono, idioma, formato o restricciones**.
   - El modelo ya sabe hacer la tarea; solo hay que orientarlo.
   - **Siempre empieza aquí.** Incluye ejemplos (*few-shot*) si hace falta.

3. **Usa RAG cuando:**
   - La respuesta depende de **información privada, específica o que cambia** (políticas, catálogos, tickets).
   - Necesitas **citas** y verificar de dónde salió la respuesta.
   - Necesitas respetar **permisos** por usuario.
   - En Foundry: **Foundry IQ**, File Search o Azure AI Search.

4. **Usa fine-tuning cuando (según la guía de Foundry):**
   - Tu prompt se volvió enorme por tantos ejemplos y casos especiales → el fine-tuning **reduce tokens y latencia**.
   - Necesitas un **estilo o tono** muy consistente (voz de marca, servicio al cliente).
   - Necesitas **formatos o esquemas** específicos de salida de forma confiable.
   - Quieres mejorar el **uso de herramientas** sin listar definiciones completas.
   - Quieres **destilar**: que un modelo pequeño y barato imite a uno grande en una tarea concreta.
   - **No** es para enseñarle "datos" que cambian: para eso es el RAG.

5. **Tipos de fine-tuning en Foundry:**

   | Tipo | Ideal para | Datos |
   |---|---|---|
   | **SFT** (Supervised Fine-Tuning) | Tareas con respuestas correctas definidas; mejorar exactitud y concisión | Pares prompt–respuesta etiquetados |
   | **DPO** (Direct Preference Optimization) | Alinear con preferencias humanas, sin modelo de recompensa separado | Respuesta preferida vs. no preferida |
   | **RFT** (Reinforcement Fine-Tuning) | Problemas complejos con muchas soluciones válidas (ej. evaluación de riesgo financiero); mejora el razonamiento | Un *grader* que califica las respuestas |

   Se pueden **apilar**: primero SFT y luego DPO.

6. **No son excluyentes:**
   ```
   System prompt (siempre)  +  RAG (si hay datos privados/cambiantes)  +  Fine-tuning (si el comportamiento no se logra con prompts)
   ```
   Un modelo ajustado puede aprender a **usar mejor** el contexto recuperado y filtrar lo irrelevante.

### Árbol de decisión
```
¿El modelo no se comporta como quieres (tono, formato, reglas)?
   └─► Mejora el SYSTEM PROMPT (+ ejemplos few-shot)
         └─► ¿Sigue fallando o el prompt es enorme y caro? ─► FINE-TUNING

¿Al modelo le falta información (privada, reciente, específica)?
   └─► RAG (Foundry IQ / Azure AI Search)

¿Necesitas citas, permisos o datos que cambian cada semana?
   └─► RAG, nunca fine-tuning
```

### Ejemplos
| Caso | Solución |
|---|---|
| "Responde siempre en español formal y en viñetas" | System prompt |
| "Contesta dudas sobre las políticas de RR. HH. que cambian cada trimestre" | RAG |
| "Clasifica tickets en nuestras 40 categorías internas con un modelo barato y rápido" | Fine-tuning (SFT) de un modelo pequeño |
| "Chatbot de una aseguradora con el tono de la marca que responde sobre las pólizas del cliente" | System prompt + RAG (+ fine-tuning si el tono no se logra) |

### Recursos
- [Cuándo usar fine-tuning en Microsoft Foundry](https://learn.microsoft.com/es-es/azure/foundry/openai/concepts/fine-tuning-considerations)

# Tema 8: ¿Para qué sí y para qué no usar la IA?

### Descripción
Que se *pueda* resolver algo con IA no significa que *se deba*. Un buen AI Engineer sabe cuándo un LLM es la herramienta correcta y cuándo basta un `if`, una consulta SQL o un servicio especializado. El examen premia la **solución más sencilla y económica** que cumple el requisito.

Analogía: la IA generativa es como una navaja suiza; sirve para casi todo, pero si vas a clavar 200 clavos, mejor usa un martillo.

### Aspectos Clave

1. **Úsala cuando:**
   - La entrada es **no estructurada** (texto libre, imágenes, audio, video).
   - Hay **muchas respuestas válidas** (redactar, resumir, traducir, conversar).
   - Las reglas son **demasiadas o cambiantes** para programarlas a mano (detectar fraude, clasificar tickets).
   - Necesitas **escalar** una tarea humana repetitiva (transcribir, extraer datos de facturas).
   - Un humano revisará el resultado o el costo de un error es bajo.

2. **No la uses (o úsala con mucho cuidado) cuando:**
   - Necesitas un resultado **exacto, determinista y auditable**: cálculo de impuestos, nómina, saldos bancarios. Usa código tradicional.
   - Las reglas son **pocas y estables**: "si el monto > 10,000, pide autorización".
   - No tienes **datos** de calidad o no tienes permiso para usarlos.
   - Un error tiene **consecuencias graves** y no hay supervisión humana (diagnóstico médico final, decisiones legales).
   - El **costo o la latencia** de llamar a un modelo no se justifica para el volumen.

3. **Matriz de decisión:**

   | Pregunta | Si la respuesta es "sí"... |
   |---|---|
   | ¿Puedo escribir la regla en menos de 10 líneas? | No uses IA |
   | ¿Existe un servicio especializado (OCR, traducción, detección de idioma)? | Úsalo antes que un LLM |
   | ¿La respuesta depende de información privada o reciente? | LLM + **RAG** |
   | ¿La tarea requiere varios pasos y tocar otros sistemas? | **Agente** |
   | ¿Un error puede dañar a una persona? | IA con **humano en el ciclo** (*human-in-the-loop*) |

4. **Riesgos a considerar siempre:**
   - **Alucinaciones:** respuestas convincentes pero falsas.
   - **Sesgo:** resultados injustos para ciertos grupos.
   - **Privacidad:** filtración de datos personales o confidenciales.
   - **Seguridad:** *prompt injection* (instrucciones maliciosas escondidas en el contenido) y *jailbreaks*.
   - **Costos:** cada token cuesta; un mal diseño puede disparar la factura.
   - **Dependencia del proveedor y versiones:** los modelos se retiran y cambian.

### Ejemplos

| Caso | ¿IA? | Por qué |
|---|---|---|
| Calcular el IVA de una factura | ❌ | Es una fórmula exacta |
| Extraer el RFC y el total de 10,000 facturas escaneadas | ✅ (Content Understanding) | Documentos no estructurados, gran volumen |
| Responder "¿cuántos días de vacaciones me tocan?" según la política interna | ✅ (LLM + RAG) | Lenguaje natural sobre información privada |
| Aprobar automáticamente un crédito hipotecario sin revisión | ⚠️ | Alto impacto: requiere transparencia, equidad y revisión humana |
| Detectar el idioma de correos entrantes para enrutarlos | ✅ (Azure Language) | Servicio especializado, determinista y barato |

### Para el examen
Recuerda la regla de oro de los exámenes de Microsoft: la respuesta correcta suele ser **la que cumple el requisito con el menor esfuerzo y el menor costo**.

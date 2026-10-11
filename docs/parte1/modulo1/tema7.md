# Tema 7: Principios de IA responsable

### Descripción
Microsoft define **seis principios de IA responsable**. En la AI-901 hay un bloque completo del examen dedicado a ellos (uno por principio), así que debes saber reconocerlos en un escenario. La IA es poderosa, pero también es probabilística, aprende de datos hechos por humanos (con sus sesgos) y puede manejar información sensible.

Analogía: los principios son como el **reglamento de tránsito** de la IA. Un coche (el modelo) puede ser muy rápido, pero sin reglas pone en riesgo a todos.

### Aspectos Clave

1. **Equidad (Fairness):**
   - **Riesgo:** los datos de entrenamiento reflejan sesgos inconscientes y el modelo discrimina.
   - **Qué hacer:** minimizar el sesgo en los datos y **probar el sistema para verificar que sea justo** entre grupos.
   - **Ejemplo:** un sistema de admisión universitaria debe evaluar con criterios académicos relevantes, no por género, edad o código postal.
   - **Pista en el examen:** "trato igualitario", "discriminación", "grupos demográficos".

2. **Confiabilidad y seguridad (Reliability and safety):**
   - **Riesgo:** la IA es probabilística, no infalible.
   - **Qué hacer:** mitigar riesgos, probar casos extremos y usar **umbrales de confianza**.
   - **Ejemplo:** un robot con visión solo toma un objeto si la confianza de la detección supera un umbral.
   - **Pista:** "fallas", "daño físico", "comportamiento consistente", "umbral".

3. **Privacidad y seguridad (Privacy and security):**
   - **Riesgo:** los datos pueden incluir información personal y el modelo podría revelarla.
   - **Qué hacer:** proteger los datos de entrenamiento y evitar que el modelo exponga datos privados.
   - **Ejemplo:** un sistema de identificación facial en aeropuerto borra las imágenes temporales en cuanto ya no se necesitan y restringe quién puede verlas.
   - **Pista:** "datos personales", "consentimiento", "acceso no autorizado".

4. **Inclusión (Inclusiveness):**
   - **Riesgo:** excluir a usuarios por discapacidad, idioma, conectividad o nivel de alfabetización.
   - **Qué hacer:** diseñar para todas las personas.
   - **Ejemplo:** un agente de voz que también genera subtítulos para personas con discapacidad auditiva.
   - **Pista:** "accesibilidad", "personas con discapacidad", "todos los usuarios".

5. **Transparencia (Transparency):**
   - **Riesgo:** que la IA parezca "magia" y los usuarios no entiendan sus límites.
   - **Qué hacer:** informar que se usa IA, cómo funciona y qué limitaciones tiene.
   - **Ejemplo:** un banco informa que usa IA para aprobar préstamos y describe las características de los datos de entrenamiento (sin revelar información confidencial).
   - **Pista:** "explicar", "informar al usuario", "limitaciones", "cómo se tomó la decisión".

6. **Responsabilidad / Rendición de cuentas (Accountability):**
   - **Riesgo:** que nadie se haga responsable cuando algo sale mal.
   - **Qué hacer:** las personas y organizaciones que desarrollan y distribuyen IA responden por ella; deben definir un **marco de gobernanza**.
   - **Ejemplo:** un comité que revisa y aprueba los casos de uso de IA y define quién responde ante un incidente.
   - **Pista:** "gobernanza", "supervisión humana", "quién es responsable".

### Truco para memorizar
**"Es Confiable, Privado, Incluyente, Transparente y Responsable"** → **E**quidad, **C**onfiabilidad, **P**rivacidad, **I**nclusión, **T**ransparencia, **R**esponsabilidad.

### Cómo se aplica en Microsoft Foundry
- **Guardrails (barreras de protección):** filtran odio, sexual, violencia y autolesiones, detectan ataques de *jailbreak* y prompts indirectos, material protegido y PII ([Parte 2, Módulo 7](../../parte2/modulo7/tema5.md)).
- **Evaluadores:** miden calidad (groundedness, relevancia, coherencia) y seguridad de modelos y agentes.
- **Model cards:** documentación de capacidades y limitaciones de cada modelo del catálogo.

### Recursos
- [Microsoft Responsible AI](https://www.microsoft.com/es-mx/ai/responsible-ai)
- [Ética, sesgos y responsabilidad en la IA (acordeón AI-900)](https://github.com/josejesusguzman/acordeon-ia-900/blob/main/docs/unidad1/comp1.md)

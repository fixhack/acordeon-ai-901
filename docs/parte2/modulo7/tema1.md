# Tema 1: Diferencia entre Foundry IQ y Work IQ

### Descripción
En Microsoft Ignite 2025 Microsoft presentó una "capa de inteligencia" para agentes compuesta por tres piezas con nombres muy parecidos: **Work IQ**, **Fabric IQ** y **Foundry IQ**. Las tres buscan dar **contexto empresarial** a los agentes, pero cada una cubre un tipo de información distinto y está pensada para un público distinto.

Analogía: imagina a un nuevo director que llega a la empresa.
- **Work IQ** es su **asistente personal**: conoce sus correos, juntas, chats, archivos y con quién trabaja.
- **Fabric IQ** es su **analista de negocio**: sabe qué significan los números de la empresa (qué es un "cliente activo", cómo se calcula el margen).
- **Foundry IQ** es la **biblioteca corporativa** con bibliotecario experto: encuentra y cita la información correcta en manuales, políticas y bases de datos, para cualquier agente que la consulte.

### Aspectos Clave

1. **Comparación:**

   | | **Work IQ** | **Fabric IQ** | **Foundry IQ** |
   |---|---|---|---|
   | ¿Qué conoce? | Datos de **trabajo** en Microsoft 365: correos, chats, reuniones, archivos, relaciones y hábitos de trabajo | **Datos de negocio** con significado semántico (ontologías, modelos semánticos de Power BI, OneLake) | **Conocimiento** de fuentes indexadas y federadas: SharePoint, Blob Storage, OneLake, web, Azure AI Search |
   | Pregunta típica | "¿Qué acordamos en la junta con Contoso y qué me falta enviar?" | "¿Qué región tuvo mayor margen el trimestre pasado?" | "¿Cuál es la política de viáticos internacionales?" |
   | ¿Quién lo usa? | Microsoft 365 Copilot y agentes que trabajan con usuarios de M365 | Personas y agentes que analizan datos de negocio | **Desarrolladores** que construyen agentes |
   | Dónde vive | Microsoft 365 (Word, Excel, Teams, Outlook) | Microsoft Fabric / Power BI | Microsoft Foundry (sobre Azure AI Search) |
   | Cómo se consume | Copilot, agentes de M365, y como fuente de conocimiento / herramienta en Foundry | Agentes de datos de Fabric, y como herramienta en Foundry | **Bases de conocimiento** expuestas como herramienta MCP |
   | Personalización | Específica de cada usuario (sus datos y permisos) | Específica del dominio de negocio | Específica del caso de uso o dominio de conocimiento |

2. **Cómo se relacionan:**
   - No compiten: son capas complementarias.
   - **Work IQ** aporta señales de **cómo opera la organización**; **Fabric IQ** aporta **significado de negocio** a los datos; **Foundry IQ** da **acceso centralizado y fundamentado** al conocimiento.
   - En Foundry, **Work IQ puede ser una fuente de conocimiento** dentro de una base de Foundry IQ y también existe como herramienta de agente ("Microsoft 365 Copilot Work IQ" aparece en la lista de fuentes del módulo).

3. **Foundry IQ en detalle (lo que pide el examen):**
   - Capa de conocimiento **administrada** sobre **Azure AI Search**.
   - **Bases de conocimiento** reutilizables por varios agentes, organizadas por dominio de negocio.
   - **Recuperación agéntica:** planea subconsultas, busca en paralelo, rankea y devuelve resultados con citas.
   - Respeta **permisos** del usuario.
   - Se conecta a los agentes como **herramienta MCP**.

4. **Work IQ en detalle:**
   - Inteligencia sobre el **trabajo de cada persona**: con quién colabora, en qué proyectos está, qué documentos usa.
   - Incluye **memoria** de hábitos y flujos de trabajo e inferencia sobre qué acción o agente conviene.
   - Es la base de que **Microsoft 365 Copilot** "conozca tu contexto".

### Para el examen
- "Un desarrollador necesita que varios agentes de Foundry respondan con documentos de SharePoint y Blob Storage, con citas y permisos" → **Foundry IQ**.
- "Un usuario de Microsoft 365 quiere que Copilot prepare su junta usando sus correos y chats" → **Work IQ**.
- "Un agente debe entender métricas de negocio definidas en modelos semánticos de Power BI" → **Fabric IQ**.

### Recursos
- [Microsoft debuts Work IQ, Fabric IQ and Foundry IQ – Cloud Wars](https://cloudwars.com/ai/microsoft-debuts-work-iq-fabric-iq-and-foundry-iq-a-unified-intelligence-layer-for-the-ai-powered-enterprise/)
- [¿Qué es Foundry IQ? – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/get-started-foundry-iq/2-explore-foundry-iq)

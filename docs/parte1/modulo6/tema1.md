# Tema 1: Fundamentos de minería de datos

### Descripción
La **minería de datos** es el proceso de descubrir patrones, relaciones y conocimiento útil en grandes volúmenes de datos. La **extracción de información** es su paso previo cuando los datos están "atrapados" en documentos, imágenes, audio o video: primero hay que convertir ese contenido no estructurado en datos estructurados, y después se pueden minar.

Analogía: es como la minería de oro. La extracción de información es sacar las piedras de la mina y separar la tierra (convertir PDFs en tablas). La minería de datos es analizar esas piedras para encontrar las pepitas (patrones de negocio).

### Aspectos Clave

1. **Tipos de datos:**

   | Tipo | Descripción | Ejemplos | ¿Cómo se analiza? |
   |---|---|---|---|
   | **Estructurados** | Esquema fijo de filas y columnas | Tablas SQL, Excel, CSV | Consultas SQL, BI, ML clásico |
   | **Semiestructurados** | Tienen etiquetas pero no esquema rígido | JSON, XML, correos (encabezados + cuerpo) | Parsers + reglas |
   | **No estructurados** | Sin formato predefinido | PDFs escaneados, fotos, audio, video, chats | OCR, NLP, visión, Content Understanding |

   Se estima que la gran mayoría de los datos de una empresa son **no estructurados**: contratos, facturas, correos, grabaciones.

2. **El proceso clásico (KDD / CRISP-DM simplificado):**
   1. **Entender el negocio:** ¿qué pregunta queremos responder? ("¿Por qué aumentaron los reembolsos?")
   2. **Recolectar datos:** bases de datos, documentos, APIs.
   3. **Extraer y transformar (ETL):** aquí entra la **extracción de información con IA** para documentos y medios.
   4. **Limpiar y preparar:** duplicados, valores faltantes, formatos (fechas, monedas).
   5. **Minar / modelar:** aplicar técnicas para encontrar patrones.
   6. **Evaluar e interpretar:** ¿el patrón es real y útil?
   7. **Desplegar:** tableros, alertas, decisiones automatizadas.

3. **Técnicas de minería de datos:**
   - **Clasificación:** asignar categorías (¿esta factura es sospechosa?).
   - **Regresión:** predecir valores (monto esperado del próximo gasto).
   - **Clustering:** agrupar por similitud (segmentos de clientes).
   - **Reglas de asociación:** "quien compra X también compra Y" (análisis de canasta).
   - **Detección de anomalías:** valores atípicos (un viático 10 veces mayor al promedio).
   - **Minería de texto:** frecuencias, temas, sentimiento, entidades.

4. **Del documento al insight: ejemplo completo**
   ```
   1,000 recibos escaneados
     → OCR + extracción de campos (Proveedor, Fecha, Total)
       → Tabla estructurada (CSV / base de datos)
         → Minería: gasto por proveedor, tendencia mensual, anomalías
           → Insight: "El 18% del gasto en taxis supera la política"
   ```

### Práctica en Python: minar datos ya extraídos
```python
import pandas as pd

# Datos como los que devolvería un extractor de recibos
recibos = pd.DataFrame([
    {"proveedor": "Fourth Coffee", "fecha": "2026-08-15", "total": 6.97,  "categoria": "alimentos"},
    {"proveedor": "Taxi Express",  "fecha": "2026-08-16", "total": 18.50, "categoria": "transporte"},
    {"proveedor": "Fourth Coffee", "fecha": "2026-08-20", "total": 7.40,  "categoria": "alimentos"},
    {"proveedor": "Taxi Express",  "fecha": "2026-08-20", "total": 22.00, "categoria": "transporte"},
    {"proveedor": "Taxi Express",  "fecha": "2026-08-21", "total": 19.00, "categoria": "transporte"},
    {"proveedor": "Taxi Express",  "fecha": "2026-08-22", "total": 95.00, "categoria": "transporte"},
    {"proveedor": "Hotel Central", "fecha": "2026-08-22", "total": 120.0, "categoria": "hospedaje"},
])
recibos["fecha"] = pd.to_datetime(recibos["fecha"])

# 1) Agregación: gasto por categoría
print(recibos.groupby("categoria")["total"].agg(["count", "sum", "mean"]))

# 2) Detección de anomalías: gastos mayores a 2x el promedio de su categoría
promedio = recibos.groupby("categoria")["total"].transform("mean")
recibos["anomalia"] = recibos["total"] > 2 * promedio
print(recibos[recibos["anomalia"]])
```
- **Explicación:**
  - `groupby` resume el gasto por categoría (minería descriptiva).
  - La regla "mayor a 2× el promedio" es una detección de anomalías sencilla; en producción usarías métodos estadísticos o modelos (Isolation Forest).
  - Nota que esta tabla **no existiría** sin la etapa previa de extracción de información.

### Consideraciones de IA responsable
- **Privacidad:** los documentos suelen tener datos personales (RFC, CURP, direcciones). Minimiza y protege.
- **Calidad:** basura entra, basura sale. Valida la confianza de cada campo extraído.
- **Equidad:** los patrones históricos pueden reflejar sesgos.

### Recursos
- [Inicio en la ciencia de datos (acordeón AI-900)](https://github.com/josejesusguzman/acordeon-ia-900/blob/main/docs/inicio_ciencia_datos.md)

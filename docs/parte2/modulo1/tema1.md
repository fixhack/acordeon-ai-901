# Tema 1: Introducción a Azure desde cero

### Descripción
**Azure** es la nube de Microsoft: un conjunto de servicios que usas por internet en lugar de comprar y mantener tus propios servidores. Pagas por lo que consumes, escalas cuando lo necesitas y delegas en Microsoft el hardware, la energía y gran parte de la seguridad física.

Analogía de Microsoft Learn: la nube de Microsoft es un **edificio de departamentos**. Tu **tenant** es tu departamento, con sus propias llaves y reglas. Dentro organizas tus cosas en cajones (**grupos de recursos**) y cada objeto es un **recurso**. La **suscripción** es el contrato de luz y agua: define quién paga y cuánto puedes consumir.

### Aspectos Clave

1. **Las cuatro categorías de servicios:**
   - **Cómputo:** "rentar computadoras en la nube" que escalan cuando quieras (VMs, contenedores, funciones).
   - **Almacenamiento:** archivos, bases de datos, imágenes, respaldos.
   - **Redes:** conectar recursos entre sí, a internet o a tu organización de forma segura.
   - **Servicios de aplicaciones:** plataformas listas para hospedar apps sin administrar servidores.

2. **Jerarquía organizacional:**
   ```
   Tenant (Microsoft Entra ID: usuarios, grupos, políticas)
    └── Suscripción (facturación, cuotas, control de acceso)
         └── Grupo de recursos (carpeta lógica)
              └── Recursos (Foundry, Storage, Key Vault, AI Search...)
   ```
   - **Tenant:** se crea cuando una organización se registra en Azure o Microsoft 365. Cada tenant está aislado.
   - **Suscripción:** liga el uso a un medio de pago (o créditos). Un tenant puede tener varias (ej. *Dev* y *Prod*).
   - **Grupo de recursos:** agrupa recursos con el mismo ciclo de vida. Si borras el grupo, borras todo lo que contiene (útil para limpiar laboratorios).
   - **Recurso:** tiene un **tipo** (ej. `Microsoft.CognitiveServices/accounts` para Foundry, `Microsoft.Storage/storageAccounts` para almacenamiento), nombre, ID, **región**, **nivel de precio** y permisos.

3. **Regiones:**
   - Ubicación física del centro de datos (ej. *East US 2*, *Sweden Central*, *Mexico Central*).
   - Afecta **latencia**, **cumplimiento** (dónde viven los datos) y **disponibilidad de modelos**: no todos los modelos de IA están en todas las regiones.

4. **Identidad y acceso:**
   - **Microsoft Entra ID:** el servicio de identidad (antes Azure Active Directory).
   - **RBAC (control de acceso basado en roles):** asignas **roles** (Owner, Contributor, Reader, **Foundry User**...) a usuarios o identidades en un **ámbito** (suscripción, grupo o recurso).
   - **Identidad administrada (managed identity):** una identidad para tu app, sin contraseñas que guardar.
   - **Azure Key Vault:** caja fuerte para **secretos** (API keys, cadenas de conexión, contraseñas).

5. **Herramientas para administrar Azure:**

   | Herramienta | Cuándo usarla |
   |---|---|
   | [Azure Portal](https://portal.azure.com) | Explorar, crear y monitorear con interfaz gráfica |
   | Azure CLI (`az`) | Automatizar con scripts |
   | Plantillas Bicep / ARM o Terraform | Infraestructura como código, repetible |
   | Portal de Foundry ([ai.azure.com](https://ai.azure.com)) | Trabajar con modelos, agentes y evaluaciones |

### Práctica: crea tu primer grupo de recursos y recurso de Foundry con Azure CLI
```bash
# 1. Iniciar sesión (abre el navegador)
az login

# 2. Ver y seleccionar la suscripción
az account list --output table
az account set --subscription "<id-o-nombre-de-suscripcion>"

# 3. Crear un grupo de recursos
az group create --name rg-acordeon-ai901 --location eastus2

# 4. Crear un recurso de Microsoft Foundry (tipo AIServices)
az cognitiveservices account create \
  --name foundry-acordeon-<tus-iniciales> \
  --resource-group rg-acordeon-ai901 \
  --kind AIServices \
  --sku S0 \
  --location eastus2 \
  --custom-domain foundry-acordeon-<tus-iniciales> \
  --allow-project-management

# 5. Ver endpoint y llaves
az cognitiveservices account show -n foundry-acordeon-<tus-iniciales> -g rg-acordeon-ai901 --query properties.endpoint
az cognitiveservices account keys list -n foundry-acordeon-<tus-iniciales> -g rg-acordeon-ai901

# 6. Al terminar tus prácticas, borra TODO para no generar costos
az group delete --name rg-acordeon-ai901 --yes --no-wait
```
- **Explicación:**
  - El recurso de Foundry es de tipo `AIServices` (proveedor `Microsoft.CognitiveServices`).
  - `--allow-project-management` habilita crear **proyectos** dentro del recurso. Si tu versión de la CLI no reconoce el parámetro, actualízala (`az upgrade`) o crea el proyecto desde el portal de Foundry, que es el camino más sencillo.
  - Borrar el grupo de recursos elimina todo lo que contiene: es la forma más segura de limpiar un laboratorio.

> [!WARNING]
> Nunca compartas tus llaves ni las subas a GitHub. Si se filtran, **regénéralas** desde el portal (*Keys and Endpoint → Regenerate*).

### Recursos
- [Fundamentos de Azure (AZ-900) en Microsoft Learn](https://learn.microsoft.com/es-es/training/paths/azure-fundamentals-describe-cloud-concepts/)
- [Crear un recurso de Microsoft Foundry con Bicep](https://learn.microsoft.com/es-es/azure/foundry/how-to/create-resource-template)

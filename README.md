# 🗣️ Forum Microservice

```
ms-forum
├─ app
│  ├─ api
│  │  └─ v1
│  │     ├─ comment_routes.py
│  │     ├─ forum_routes.py
│  │     ├─ reaction_routes.py
│  │     ├─ __init__.py
│  │     └─ __pycache__
│  ├─ core
│  │  ├─ config.py
│  │  ├─ security.py
│  │  └─ __pycache__
│  ├─ db
│  │  ├─ mongodb.py
│  │  └─ __pycache__
│  ├─ main.py
│  ├─ models
│  │  ├─ attachment_model.py
│  │  ├─ comment__model.py
│  │  ├─ post_model.py
│  │  ├─ reaction_model.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  ├─ schemas
│  │  ├─ comment_schema.py
│  │  ├─ post_schema.py
│  │  ├─ reaction_schema.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  ├─ services
│  │  ├─ attachment_service.py
│  │  ├─ comment_service.py
│  │  ├─ post_service.py
│  │  ├─ reaction_service.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  ├─ __init__.py
│  └─ __pycache__
├─ Dockerfile
├─ LICENSE
├─ pytest.ini
├─ README.md
├─ requirements.txt
└─ tests
   ├─ conftest.py
   ├─ test_comment_routes.py
   ├─ test_connection.py
   ├─ test_forum_routes.py
   ├─ test_post_model.py
   ├─ test_post_service.py
   ├─ test_reaction_routes.py
   ├─ __init__.py
   └─ __pycache__

```

Microservicio de foro para gestionar posts, comentarios y reacciones, construido con FastAPI y MongoDB.

## 📋 Requisitos Previos

- Python 3.8 o superior
- MongoDB Atlas (o MongoDB local)
- pip (gestor de paquetes de Python)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio (si aún no lo has hecho)

```bash
git clone <url-del-repositorio>
cd ms-forum
```

### 2. Crear y activar el entorno virtual

**En Windows (PowerShell):**

```powershell
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
.\venv\Scripts\Activate
```

**En Linux/Mac:**

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente configuración:

```env
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
```

> **Nota:** Reemplaza `usuario`, `password` y `cluster` con tus credenciales reales de MongoDB Atlas.

### 5. Ejecutar la API

```bash
uvicorn app.main:app --reload
```

O especificando host y puerto:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Verificar que la API está corriendo

Una vez iniciada, la API estará disponible en:

- **URL base:** http://localhost:8000
- **Documentación interactiva (Swagger UI):** http://localhost:8000/docs
- **Documentación alternativa (ReDoc):** http://localhost:8000/redoc
- **Health check:** http://localhost:8000/health

## 📚 Endpoints Disponibles

### Posts del Foro

- `GET/POST /orgs/{org_id}/forum/` - Listar y crear posts

### Comentarios

- `GET/POST /orgs/{org_id}/forum/posts/{post_id}/comments/` - Gestionar comentarios

### Reacciones

- `POST /orgs/{org_id}/forum/posts/{post_id}/reactions/` - Agregar reacciones (likes/dislikes)

### Archivos Estáticos

- `GET /files/{filename}` - Acceder a archivos subidos

## 🧪 Ejecutar Tests

```bash
pytest
```

## 🐳 Ejecutar con Docker (Opcional)

```bash
# Construir la imagen
docker build -t ms-forum .

# Ejecutar el contenedor
docker run -p 8000:8000 --env-file .env ms-forum
```

## 📝 Notas Adicionales

- El microservicio utiliza **MongoEngine** como ODM para MongoDB
- Los archivos subidos se almacenan en la carpeta `uploads/`
- CORS está configurado para permitir todas las orígenes (ajustar en producción)

## 🛠️ Tecnologías Utilizadas

- **FastAPI** - Framework web moderno y rápido
- **MongoDB** - Base de datos NoSQL
- **MongoEngine** - ODM para MongoDB
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validación de datos
- **PyJWT** - Manejo de tokens JWT

## ☁️ Despliegue en Google Cloud Run

### Requisitos Previos

1. **Google Cloud CLI** instalado y configurado

   ```bash
   # Instalar gcloud CLI (si no lo tienes)
   # https://cloud.google.com/sdk/docs/install

   # Inicializar y autenticar
   gcloud init
   gcloud auth login
   ```

2. **Proyecto de Google Cloud** configurado

   ```bash
   # Configurar el proyecto
   gcloud config set project YOUR_PROJECT_ID

   # Habilitar APIs necesarias
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

3. **MongoDB** en producción (recomendado: MongoDB Atlas)
   - Crea un cluster en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Configura las reglas de red para permitir conexiones desde cualquier IP (0.0.0.0/0) o especifica las IPs de Cloud Run
   - Obtén tu connection string (MONGO_URI)

### Variables de Entorno

Antes de desplegar, configura las siguientes variables de entorno:

```bash
# MONGO_URI: Connection string de MongoDB Atlas
export MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/forum_db?retryWrites=true&w=majority"

# JWT_SECRET_KEY: Clave secreta para JWT (genera una segura)
export JWT_SECRET_KEY=$(openssl rand -hex 32)
```

### Despliegue con Cloud Run

#### Opción 1: Despliegue Directo desde el Código Fuente

```bash
# Desde la raíz del proyecto ms-forum
gcloud run deploy ms-forum \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONGO_URI="${MONGO_URI}",JWT_SECRET_KEY="${JWT_SECRET_KEY}" \
  --port 8080
```

#### Opción 2: Build y Deploy con Container Registry

```bash
# 1. Configurar variables
export PROJECT_ID=$(gcloud config get-value project)
export IMAGE_NAME="gcr.io/${PROJECT_ID}/ms-forum"

# 2. Construir la imagen Docker
docker build -t ${IMAGE_NAME} .

# 3. Subir la imagen a Container Registry
docker push ${IMAGE_NAME}

# 4. Desplegar en Cloud Run
gcloud run deploy ms-forum \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONGO_URI="${MONGO_URI}",JWT_SECRET_KEY="${JWT_SECRET_KEY}"
```

#### Opción 3: Despliegue desde GitHub (Recomendado para CI/CD)

1. Conecta tu repositorio en la consola de Google Cloud
2. Ve a Cloud Run > Create Service > Deploy from Source Repository
3. Selecciona tu repositorio y rama
4. Configura las variables de entorno en la consola
5. Google Cloud Build se encargará del resto

### Verificar el Despliegue

Después del despliegue, obtendrás una URL como:

```
https://ms-forum-xxxxx-uc.a.run.app
```

Verifica que el servicio está funcionando:

```bash
# Health check
curl https://ms-forum-xxxxx-uc.a.run.app/health

# Documentación API
# Abre en tu navegador:
https://ms-forum-xxxxx-uc.a.run.app/docs
```

### Configuración Avanzada

#### Escalar el Servicio

```bash
gcloud run services update ms-forum \
  --min-instances 0 \
  --max-instances 10 \
  --cpu 1 \
  --memory 512Mi
```

#### Actualizar Variables de Entorno

```bash
gcloud run services update ms-forum \
  --update-env-vars NEW_VAR=value
```

#### Ver Logs

```bash
gcloud run services logs read ms-forum --limit 50
```

### Consideraciones de Producción

> **⚠️ CORS:** Actualiza la configuración de CORS en `app/main.py` para permitir solo tus dominios en producción:
>
> ```python
> allow_origins=["https://tu-frontend.com"],
> ```

> **⚠️ Almacenamiento de Archivos:** Cloud Run es stateless y efímero. Los archivos subidos a `/uploads` se perderán al reiniciar el contenedor. Para producción, considera usar **Google Cloud Storage** para almacenar archivos de forma persistente.

> **⚠️ Secrets:** Para mayor seguridad, usa **Secret Manager** en lugar de variables de entorno para información sensible:
>
> ```bash
> # Crear secret
> echo -n "tu-secret-key" | gcloud secrets create jwt-secret --data-file=-
>
> # Usar en Cloud Run
> gcloud run deploy ms-forum \
>   --set-secrets JWT_SECRET_KEY=jwt-secret:latest
> ```

### Monitoreo

Accede a los logs y métricas en la consola de Google Cloud:

- **Logs:** Cloud Run > ms-forum > Logs
- **Métricas:** Cloud Run > ms-forum > Metrics

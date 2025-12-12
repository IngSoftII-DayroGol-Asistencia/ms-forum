# 🗣️ Forum Microservice

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
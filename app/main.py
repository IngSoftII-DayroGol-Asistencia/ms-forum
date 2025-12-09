from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.db.mongodb import init_db
from app.api.v1 import forum_routes
from app.api.v1 import comment_routes
from app.api.v1 import reaction_routes

app = FastAPI(
    title="Forum Microservice",
    description="API para gestionar un foro con posts, comentarios y reacciones",
    version="1.0.0"
)

# Configurar CORS (importante para el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos
init_db()

# Rutas del foro (posts)
app.include_router(forum_routes.router)

# Rutas de comentarios
app.include_router(comment_routes.router)

# Rutas de reacciones (likes/dislikes)
app.include_router(reaction_routes.router)

# Montar carpeta de archivos estáticos
app.mount("/files", StaticFiles(directory="uploads"), name="files")

@app.get("/")
def root():
    return {
        "message": "Forum API is running",
        "version": "1.0.0",
        "endpoints": {
            "posts": "/orgs/{org_id}/forum/",
            "comments": "/orgs/{org_id}/forum/posts/{post_id}/comments/",
            "reactions": "/orgs/{org_id}/forum/posts/{post_id}/reactions/",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
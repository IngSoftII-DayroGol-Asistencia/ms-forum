# app/main.py
from fastapi import FastAPI
from app.db.mongodb import init_db
from app.api.v1 import forum_routes

app = FastAPI(title="Forum Microservice")

# Conexión a MongoDB
init_db()

# Registrar las rutas
app.include_router(forum_routes.router)

@app.get("/")
def root():
    return {"message": "Forum API is running"}


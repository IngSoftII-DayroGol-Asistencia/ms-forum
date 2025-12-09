from mongoengine import connect
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URI de conexión a MongoDB Atlas
uri = os.getenv("MONGO_URI")  

# Función para inicializar la conexión con MongoEngine
def init_db():
    try:
        # Conectar usando MongoEngine 
        connect(
            db='forum_db',  
            host=uri,
            uuidRepresentation='standard'
        )
        print("✅ Successfully connected to MongoDB Atlas with MongoEngine!")
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
from mongoengine import connect, disconnect
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Cargar variables de entorno desde la raíz del proyecto
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# URI de conexión a MongoDB Atlas
uri = os.getenv("MONGO_URI")  

def init_db():
    """
    Inicializa la conexión con MongoDB Atlas usando MongoEngine
    """
    if not uri:
        print("❌ ERROR: MONGO_URI no está definida en el archivo .env")
        sys.exit(1)
    
    try:
        # Desconectar cualquier conexión previa
        disconnect()
        
        # Conectar usando MongoEngine con configuración mejorada
        connect(
            db='forum_db',  
            host=uri,
            uuidRepresentation='standard',
            serverSelectionTimeoutMS=5000,  
            connectTimeoutMS=10000,          
            socketTimeoutMS=10000,           
            maxPoolSize=10,                  
            retryWrites=True
        )
        print("✅ Successfully connected to MongoDB Atlas with MongoEngine!")
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión a MongoDB: {str(e)}")
        print(f"   URI utilizada: {uri[:30]}...")  
        print("\n🔍 Posibles soluciones:")
        print("   1. Verifica que tu IP esté en la whitelist de MongoDB Atlas")
        print("   2. Asegúrate que el cluster esté activo (no pausado)")
        print("   3. Verifica que las credenciales sean correctas")
        print("   4. Revisa tu conexión a internet")
        return False


def test_connection():
    """
    Prueba la conexión a MongoDB
    """
    try:
        from mongoengine import connect
        client = connect(
            db='forum_db',
            host=uri,
            serverSelectionTimeoutMS=3000
        )
        # Intenta hacer una operación simple
        client.server_info()
        print("✅ Conexión exitosa!")
        return True
    except Exception as e:
        print(f"❌ Error en test de conexión: {str(e)}")
        return False
"""
Script para probar la conexión a MongoDB Atlas
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")

if not uri:
    print("❌ ERROR: MONGO_URI no está definida en .env")
    print("   Verifica que el archivo .env esté en la raíz del proyecto")
    exit(1)

print("🔍 Probando conexión a MongoDB Atlas...")
print(f"URI: {uri[:40]}...\n")

try:
    # Intenta conectar con timeout corto
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # Prueba la conexión
    client.admin.command('ping')
    
    print("✅ ¡Conexión exitosa a MongoDB Atlas!")
    
    # Muestra información del servidor
    server_info = client.server_info()
    print(f"\n📊 Información del servidor:")
    print(f"   - Versión MongoDB: {server_info.get('version')}")
    
    # Lista las bases de datos
    print(f"\n📁 Bases de datos disponibles:")
    for db_name in client.list_database_names():
        print(f"   - {db_name}")
    
    # Verifica la base de datos forum_db
    db = client['forum_db']
    collections = db.list_collection_names()
    print(f"\n📚 Colecciones en 'forum_db':")
    if collections:
        for coll in collections:
            print(f"   - {coll}")
    else:
        print("   - (No hay colecciones aún)")
    
    client.close()
    
except Exception as e:
    print(f"❌ Error de conexión: {str(e)}\n")
    print("🔧 Soluciones posibles:")
    print("   1. Ve a MongoDB Atlas > Network Access")
    print("   2. Agrega tu IP actual o permite 0.0.0.0/0")
    print("   3. Verifica que el cluster esté activo (punto verde)")
    print("   4. Revisa tus credenciales en el archivo .env")
    print("   5. Asegúrate de tener conexión a internet")
from pydantic import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    MONGO_URI: str
    HOST: str = "0.0.0.0"  # Default host
    PORT: int = 4000  # Default port

    class ConfigDict:
        env_file = ".env"  # Cargar las variables de entorno desde el archivo .env

settings = Settings()

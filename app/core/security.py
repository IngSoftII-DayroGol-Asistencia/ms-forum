import jwt
from datetime import datetime, timedelta
from app.core.config import settings

# Crear un JWT
def create_jwt_token(data: dict):
    expiration = timedelta(hours=1)  # El token expirará en 1 hora
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expiration})  # Agregar la fecha de expiración
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

# Verificar el JWT
def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload  # Devuelve el payload (información) si es válido
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

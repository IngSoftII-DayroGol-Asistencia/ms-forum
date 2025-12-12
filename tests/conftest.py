"""
Configuración compartida para todos los tests
Fixtures reutilizables y setup/teardown
"""
import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from bson import ObjectId
from pathlib import Path

# Agregar el directorio raíz al path de Python
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Mock de MongoEngine ANTES de cualquier import
mock_mongoengine = MagicMock()
sys.modules['mongoengine'] = mock_mongoengine

# Mock de la conexión a MongoDB
@pytest.fixture(autouse=True)
def mock_mongodb_connection():
    """Mock automático de MongoDB para todos los tests"""
    with patch('app.db.mongodb.connect') as mock_connect, \
         patch('app.db.mongodb.disconnect') as mock_disconnect, \
         patch('app.db.mongodb.init_db', return_value=True):
        yield mock_connect

@pytest.fixture
def client():
    """Cliente de prueba de FastAPI"""
    # Importar aquí para evitar problemas de import circular
    from fastapi.testclient import TestClient
    
    # Mock de init_db antes de importar la app
    with patch('app.db.mongodb.init_db', return_value=True):
        from app.main import app  
        return TestClient(app)

@pytest.fixture
def mock_post():
    """Post mock para testing"""
    post = Mock()
    post.id = ObjectId()
    post.organization_id = "org_123"
    post.user_id = "user_123"
    post.title = "Test Post"
    post.content = "Test content"
    post.created_at = datetime.utcnow()
    post.updated_at = datetime.utcnow()
    post.likes_count = 0
    post.dislikes_count = 0
    post.comments_count = 0
    post.attachments = []
    
    # Mock de métodos
    post.save = Mock()
    post.delete = Mock()
    post.reload = Mock()
    post.update = Mock()
    post.to_mongo = Mock(return_value={
        '_id': post.id,
        'organization_id': post.organization_id,
        'user_id': post.user_id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at,
        'updated_at': post.updated_at,
        'likes_count': 0,
        'dislikes_count': 0,
        'comments_count': 0
    })
    
    return post

@pytest.fixture
def mock_comment():
    """Comment mock para testing"""
    comment = Mock()
    comment.id = ObjectId()
    comment.user_name = "Test User"
    comment.content = "Test comment content"
    comment.created_at = datetime.utcnow()
    
    # Mock del post asociado
    comment.post = Mock()
    comment.post.id = ObjectId()
    
    # Mock de métodos
    comment.save = Mock()
    comment.delete = Mock()
    comment.reload = Mock()
    
    return comment

@pytest.fixture
def mock_reaction():
    """Reaction mock para testing"""
    reaction = Mock()
    reaction.id = ObjectId()
    reaction.user_id = "user_123"
    reaction.reaction_type = "like"
    reaction.created_at = datetime.utcnow()
    
    # Mock del post asociado
    reaction.post = Mock()
    reaction.post.id = ObjectId()
    reaction.post.likes_count = 1
    reaction.post.dislikes_count = 0
    
    # Mock de métodos
    reaction.save = Mock()
    reaction.delete = Mock()
    reaction.update = Mock()
    
    return reaction

@pytest.fixture
def mock_attachment():
    """Attachment mock para testing"""
    attachment = Mock()
    attachment.id = ObjectId()
    attachment.file_name = "test_file.pdf"
    attachment.stored_name = "uuid_test_file.pdf"
    attachment.content_type = "application/pdf"
    attachment.size_bytes = 1024
    attachment.created_at = datetime.utcnow()
    
    attachment.save = Mock()
    
    return attachment

@pytest.fixture
def sample_post_data():
    """Datos de ejemplo para crear un post"""
    return {
        "title": "Test Post Title",
        "content": "This is test content for the post",
        "user_id": "user_123"
    }

@pytest.fixture
def sample_comment_data():
    """Datos de ejemplo para crear un comentario"""
    return {
        "user_name": "John Doe",
        "content": "This is a test comment"
    }

@pytest.fixture
def sample_reaction_data():
    """Datos de ejemplo para crear una reacción"""
    return {
        "user_id": "user_123",
        "reaction_type": "like"
    }

@pytest.fixture
def mock_upload_file():
    """Mock de UploadFile para testing de attachments"""
    from io import BytesIO
    
    file = Mock()
    file.filename = "test_document.pdf"
    file.content_type = "application/pdf"
    file.file = BytesIO(b"fake file content")
    
    return file

# Fixture para crear directorio uploads si no existe
@pytest.fixture(autouse=True)
def setup_uploads_dir():
    """Crear directorio uploads para tests"""
    uploads_dir = ROOT_DIR / "uploads"
    uploads_dir.mkdir(exist_ok=True)
    yield
    # Cleanup no es necesario para tests unitarios
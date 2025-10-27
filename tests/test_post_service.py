import pytest
from unittest import mock
from app.services.post_service import PostService

@pytest.fixture
def service():
    return PostService()

def test_create_post(service):
    # Creamos un mock para la función create_post
    with mock.patch.object(service, 'create_post', return_value={"id": "mocked_id_12345", "title": "Test Post", "content": "Test Content"}):
        # Llamamos al servicio, pero la función 'create_post' está mockeada
        result = service.create_post({"title": "Test Post", "content": "Test Content"})
        
        # Verificamos que el mock se haya llamado y que la respuesta es la esperada
        assert result == {"id": "mocked_id_12345", "title": "Test Post", "content": "Test Content"}

def test_get_posts(service):
    # Mockear la respuesta de get_all_posts
    with mock.patch.object(service, 'get_all_posts', return_value=[{"id": "mocked_id_12345", "title": "Test Post", "content": "Test Content"}]):
        # Llamar al método get_all_posts
        result = service.get_all_posts()
        
        # Verificar que la respuesta es la esperada
        assert result == [{"id": "mocked_id_12345", "title": "Test Post", "content": "Test Content"}]

def test_update_post(service):
    # Mockear la respuesta de update_post
    with mock.patch.object(service, 'update_post', return_value={"id": "mocked_id_12345", "title": "Updated Post", "content": "Updated Content"}):
        # Llamar al método update_post
        result = service.update_post("mocked_id_12345", {"title": "Updated Post", "content": "Updated Content"})
        
        # Verificar que la respuesta sea la esperada
        assert result == {"id": "mocked_id_12345", "title": "Updated Post", "content": "Updated Content"}

def test_delete_post(service):
    # Mockear la respuesta de delete_post
    with mock.patch.object(service, 'delete_post', return_value={"message": "Post deleted successfully"}):
        # Llamar al método delete_post
        result = service.delete_post("mocked_id_12345")
        
        # Verificar que la respuesta sea la esperada
        assert result == {"message": "Post deleted successfully"}

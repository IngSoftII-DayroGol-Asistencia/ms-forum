"""
Tests para las rutas del foro (forum_routes.py)
Verifican los endpoints de la API para posts
"""
import pytest
from unittest.mock import Mock, patch
from io import BytesIO

class TestForumRoutes:
    """Tests para las rutas del foro"""
    
    @patch('app.api.v1.forum_routes.service.create_post')
    def test_create_post_success(self, mock_create, client, mock_post, sample_post_data):
        """Test: POST /orgs/{org_id}/forum/ - Crear post exitosamente"""
        # Arrange
        mock_create.return_value = mock_post
        
        # Act
        response = client.post(
            "/orgs/org_123/forum/",
            data=sample_post_data
        )
        
        # Assert
        assert response.status_code == 200
        assert "id" in response.json()
    
    @patch('app.api.v1.forum_routes.service.get_all_posts')
    def test_get_all_posts(self, mock_get_all, client, mock_post):
        """Test: GET /orgs/{org_id}/forum/ - Obtener todos los posts"""
        # Arrange
        mock_post.to_mongo = Mock(return_value={
            '_id': mock_post.id,
            'organization_id': 'org_123',
            'title': 'Test',
            'content': 'Content'
        })
        mock_get_all.return_value = [mock_post]
        
        # Act
        response = client.get("/orgs/org_123/forum/")
        
        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1
    
    @patch('app.api.v1.forum_routes.service.get_post_by_id')
    def test_get_post_by_id_success(self, mock_get_by_id, client, mock_post):
        """Test: GET /orgs/{org_id}/forum/{post_id} - Obtener post por ID"""
        # Arrange
        post_id = str(mock_post.id)
        mock_post.to_mongo = Mock(return_value={
            '_id': mock_post.id,
            'organization_id': 'org_123',
            'title': 'Test',
            'content': 'Content'
        })
        mock_get_by_id.return_value = mock_post
        
        # Act
        response = client.get(f"/orgs/org_123/forum/{post_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Post"
    
    @patch('app.api.v1.forum_routes.service.get_post_by_id')
    def test_get_post_not_found(self, mock_get_by_id, client):
        """Test: GET post inexistente retorna 404"""
        # Arrange
        mock_get_by_id.side_effect = Exception("Post not found")
        
        # Act
        response = client.get("/orgs/org_123/forum/invalid_id")
        
        # Assert
        assert response.status_code == 404
    
    @patch('app.api.v1.forum_routes.service.update_post')
    @patch('app.api.v1.forum_routes.service.get_post_by_id')
    def test_update_post_success(self, mock_get, mock_update, client, mock_post):
        """Test: PUT /orgs/{org_id}/forum/{post_id} - Actualizar post"""
        # Arrange
        post_id = str(mock_post.id)
        mock_post.to_mongo = Mock(return_value={
            '_id': mock_post.id,
            'organization_id': 'org_123',
            'title': 'Updated Title',
            'content': 'Content'
        })
        mock_post.title = "Updated Title"
        mock_update.return_value = mock_post
        
        update_data = {"title": "Updated Title"}
        
        # Act
        response = client.put(
            f"/orgs/org_123/forum/{post_id}",
            json=update_data
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
    
    @patch('app.api.v1.forum_routes.service.delete_post')
    def test_delete_post_success(self, mock_delete, client, mock_post):
        """Test: DELETE /orgs/{org_id}/forum/{post_id} - Eliminar post"""
        # Arrange
        post_id = str(mock_post.id)
        mock_delete.return_value = {"message": "Post deleted successfully"}
        
        # Act
        response = client.delete(f"/orgs/org_123/forum/{post_id}")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Post deleted successfully"
    
    @patch('app.api.v1.forum_routes.attachment_service.attach_file_to_post')
    @patch('app.api.v1.forum_routes.service.get_post_by_id')
    def test_upload_attachment(self, mock_get_post, mock_attach, client, mock_post, mock_attachment):
        """Test: POST /orgs/{org_id}/forum/{post_id}/upload - Subir archivo"""
        # Arrange
        post_id = str(mock_post.id)
        mock_get_post.return_value = mock_post
        mock_attach.return_value = mock_attachment
        
        # Crear archivo de prueba
        file_content = b"fake file content"
        files = {"file": ("test.pdf", BytesIO(file_content), "application/pdf")}
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/{post_id}/upload",
            files=files
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "file_name" in data
        assert data["file_name"] == "test_file.pdf"
    
    @patch('app.api.v1.forum_routes.service.create_post')
    def test_create_post_validation_error(self, mock_create, client):
        """Test: Crear post sin título retorna error de validación"""
        # Arrange
        invalid_data = {"content": "Content without title"}
        
        # Act
        response = client.post(
            "/orgs/org_123/forum/",
            data=invalid_data
        )
        
        # Assert
        assert response.status_code == 422  # Validation error
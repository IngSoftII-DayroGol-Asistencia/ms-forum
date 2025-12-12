"""
Tests para las rutas de comentarios (comment_routes.py)
Verifican los endpoints de la API para comentarios
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from datetime import datetime

class TestCommentRoutes:
    """Tests para las rutas de comentarios"""
    
    @patch('app.api.v1.comment_routes.comment_service.create_comment')
    def test_create_comment_success(self, mock_create, client, mock_comment, sample_comment_data):
        """Test: POST /orgs/{org_id}/forum/posts/{post_id}/comments/ - Crear comentario"""
        # Arrange
        mock_create.return_value = mock_comment
        post_id = "507f1f77bcf86cd799439011"
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/comments/",
            json=sample_comment_data
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["user_name"] == mock_comment.user_name
        assert data["content"] == mock_comment.content
    
    @patch('app.api.v1.comment_routes.comment_service.get_comments_for_post')
    def test_get_comments_for_post(self, mock_get_comments, client, mock_comment):
        """Test: GET /orgs/{org_id}/forum/posts/{post_id}/comments/ - Obtener comentarios"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        mock_get_comments.return_value = [mock_comment]
        
        # Act
        response = client.get(f"/orgs/org_123/forum/posts/{post_id}/comments/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["user_name"] == mock_comment.user_name
    
    @patch('app.api.v1.comment_routes.comment_service.get_comments_for_post')
    def test_get_comments_empty_list(self, mock_get_comments, client):
        """Test: Obtener comentarios cuando no hay ninguno"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        mock_get_comments.return_value = []
        
        # Act
        response = client.get(f"/orgs/org_123/forum/posts/{post_id}/comments/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []
    
    @patch('app.api.v1.comment_routes.comment_service.delete_comment')
    def test_delete_comment_success(self, mock_delete, client):
        """Test: DELETE /orgs/{org_id}/forum/posts/{post_id}/comments/{comment_id}"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        comment_id = "507f1f77bcf86cd799439012"
        mock_delete.return_value = {"message": "Comment deleted successfully"}
        
        # Act
        response = client.delete(
            f"/orgs/org_123/forum/posts/{post_id}/comments/{comment_id}"
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Comment deleted successfully"
    
    @patch('app.api.v1.comment_routes.comment_service.create_comment')
    def test_create_comment_invalid_post(self, mock_create, client, sample_comment_data):
        """Test: Crear comentario en post inexistente"""
        # Arrange
        mock_create.side_effect = HTTPException(status_code=404, detail="Post not found")
        post_id = "invalid_id"
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/comments/",
            json=sample_comment_data
        )
        
        # Assert
        assert response.status_code == 404
    
    @patch('app.api.v1.comment_routes.comment_service.create_comment')
    def test_create_comment_validation_error(self, mock_create, client):
        """Test: Crear comentario sin campos requeridos"""
        # Arrange
        invalid_data = {"user_name": "John"}  # Falta 'content'
        post_id = "507f1f77bcf86cd799439011"
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/comments/",
            json=invalid_data
        )
        
        # Assert
        assert response.status_code == 422  # Validation error
    
    @patch('app.api.v1.comment_routes.comment_service.delete_comment')
    def test_delete_comment_not_found(self, mock_delete, client):
        """Test: Eliminar comentario inexistente"""
        # Arrange
        mock_delete.side_effect = HTTPException(status_code=404, detail="Comment not found")
        post_id = "507f1f77bcf86cd799439011"
        comment_id = "invalid_id"
        
        # Act
        response = client.delete(
            f"/orgs/org_123/forum/posts/{post_id}/comments/{comment_id}"
        )
        
        # Assert
        assert response.status_code == 404
    
    @patch('app.api.v1.comment_routes.comment_service.create_comment')
    def test_create_comment_with_long_content(self, mock_create, client, mock_comment):
        """Test: Crear comentario con contenido largo"""
        # Arrange
        mock_create.return_value = mock_comment
        post_id = "507f1f77bcf86cd799439011"
        long_content = "A" * 1000  # 1000 caracteres
        comment_data = {
            "user_name": "John Doe",
            "content": long_content
        }
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/comments/",
            json=comment_data
        )
        
        # Assert
        assert response.status_code == 201
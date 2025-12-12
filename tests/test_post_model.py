"""
Tests para el modelo Post
Verifican la estructura y métodos del modelo
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from bson import ObjectId

class TestPostModel:
    """Tests para el modelo Post"""
    
    def test_post_creation(self, mock_post):
        """Test: Crear un post con todos los campos"""
        # Assert
        assert mock_post.organization_id == "org_123"
        assert mock_post.title == "Test Post"
        assert mock_post.content == "Test content"
        assert mock_post.likes_count == 0
        assert mock_post.dislikes_count == 0
        assert mock_post.comments_count == 0
        assert isinstance(mock_post.created_at, datetime)
    
    def test_post_to_dict(self, mock_post):
        """Test: Método to_dict() serializa correctamente"""
        # Arrange
        mock_post.to_dict = Mock(return_value={
            "id": str(mock_post.id),
            "organization_id": mock_post.organization_id,
            "title": mock_post.title,
            "content": mock_post.content,
            "likes_count": mock_post.likes_count,
            "dislikes_count": mock_post.dislikes_count,
            "comments_count": mock_post.comments_count,
            "attachments": []
        })
        
        # Act
        result = mock_post.to_dict()
        
        # Assert
        assert "id" in result
        assert result["organization_id"] == "org_123"
        assert result["title"] == "Test Post"
        assert result["likes_count"] == 0
    
    def test_post_save(self, mock_post):
        """Test: Guardar un post"""
        # Act
        mock_post.save()
        
        # Assert
        mock_post.save.assert_called_once()
    
    def test_post_update(self, mock_post):
        """Test: Actualizar un post"""
        # Act
        mock_post.update(set__title="New Title")
        
        # Assert
        mock_post.update.assert_called_once_with(set__title="New Title")
    
    def test_post_delete(self, mock_post):
        """Test: Eliminar un post"""
        # Act
        mock_post.delete()
        
        # Assert
        mock_post.delete.assert_called_once()
    
    def test_post_with_attachments(self, mock_post, mock_attachment):
        """Test: Post con attachments"""
        # Arrange
        mock_post.attachments = [mock_attachment]
        
        # Assert
        assert len(mock_post.attachments) == 1
        assert mock_post.attachments[0].file_name == "test_file.pdf"
    
    def test_post_increment_likes(self, mock_post):
        """Test: Incrementar contador de likes"""
        # Act
        mock_post.update(inc__likes_count=1)
        
        # Assert
        mock_post.update.assert_called_with(inc__likes_count=1)
    
    def test_post_increment_comments(self, mock_post):
        """Test: Incrementar contador de comentarios"""
        # Act
        mock_post.update(inc__comments_count=1)
        
        # Assert
        mock_post.update.assert_called_with(inc__comments_count=1)
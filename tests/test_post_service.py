"""
Tests para PostService
Verifican la lógica de negocio del servicio de posts
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from bson import ObjectId

class TestPostService:
    """Tests para el servicio de posts"""
    
    @patch('app.services.post_service.Post')
    def test_create_post_success(self, mock_post_class, sample_post_data, mock_post):
        """Test: Crear un post exitosamente"""
        # Arrange
        from app.services.post_service import PostService
        from app.schemas.post_schema import PostCreate
        
        mock_post_class.return_value = mock_post
        service = PostService()
        post_data = PostCreate(**sample_post_data)
        
        # Act
        result = service.create_post("org_123", post_data)
        
        # Assert
        mock_post.save.assert_called_once()
        assert result == mock_post
    
    @patch('app.services.post_service.Post')
    def test_get_all_posts(self, mock_post_class, mock_post):
        """Test: Obtener todos los posts de una organización"""
        # Arrange
        from app.services.post_service import PostService
        
        mock_post_class.objects.return_value.all.return_value = [mock_post]
        service = PostService()
        
        # Act
        result = service.get_all_posts("org_123")
        
        # Assert
        mock_post_class.objects.assert_called_once_with(organization_id="org_123")
        assert len(result) == 1
        assert result[0] == mock_post
    
    @patch('app.services.post_service.Post')
    @patch('app.services.post_service.ObjectId')
    def test_get_post_by_id_success(self, mock_objectid, mock_post_class, mock_post):
        """Test: Obtener un post por ID exitosamente"""
        # Arrange
        from app.services.post_service import PostService
        
        post_id = ObjectId()
        mock_objectid.return_value = post_id
        mock_post_class.objects.return_value.first.return_value = mock_post
        service = PostService()
        
        # Act
        result = service.get_post_by_id("org_123", str(post_id))
        
        # Assert
        assert result == mock_post
    
    @patch('app.services.post_service.Post')
    @patch('app.services.post_service.ObjectId')
    def test_get_post_by_id_not_found(self, mock_objectid, mock_post_class):
        """Test: Post no encontrado lanza excepción"""
        # Arrange
        from app.services.post_service import PostService
        
        post_id = ObjectId()
        mock_objectid.return_value = post_id
        mock_post_class.objects.return_value.first.return_value = None
        service = PostService()
        
        # Act & Assert
        with pytest.raises(Exception, match="Post not found"):
            service.get_post_by_id("org_123", str(post_id))
    
    @patch('app.services.post_service.Post')
    @patch('app.services.post_service.ObjectId')
    def test_update_post_title(self, mock_objectid, mock_post_class, mock_post):
        """Test: Actualizar el título de un post"""
        # Arrange
        from app.services.post_service import PostService
        from app.schemas.post_schema import PostUpdate
        
        post_id = ObjectId()
        mock_objectid.return_value = post_id
        mock_post_class.objects.return_value.first.return_value = mock_post
        service = PostService()
        update_data = PostUpdate(title="New Title")
        
        # Act
        result = service.update_post("org_123", str(post_id), update_data)
        
        # Assert
        mock_post.update.assert_called_with(set__title="New Title")
        mock_post.reload.assert_called_once()
        assert result == mock_post
    
    @patch('app.services.post_service.Post')
    @patch('app.services.post_service.ObjectId')
    def test_update_post_content(self, mock_objectid, mock_post_class, mock_post):
        """Test: Actualizar el contenido de un post"""
        # Arrange
        from app.services.post_service import PostService
        from app.schemas.post_schema import PostUpdate
        
        post_id = ObjectId()
        mock_objectid.return_value = post_id
        mock_post_class.objects.return_value.first.return_value = mock_post
        service = PostService()
        update_data = PostUpdate(content="New content")
        
        # Act
        result = service.update_post("org_123", str(post_id), update_data)
        
        # Assert
        mock_post.update.assert_called_with(set__content="New content")
    
    @patch('app.services.post_service.Post')
    @patch('app.services.post_service.ObjectId')
    def test_delete_post_success(self, mock_objectid, mock_post_class, mock_post):
        """Test: Eliminar un post exitosamente"""
        # Arrange
        from app.services.post_service import PostService
        
        post_id = ObjectId()
        mock_objectid.return_value = post_id
        mock_post_class.objects.return_value.first.return_value = mock_post
        service = PostService()
        
        # Act
        result = service.delete_post("org_123", str(post_id))
        
        # Assert
        mock_post.delete.assert_called_once()
        assert result == {"message": "Post deleted successfully"}
    
    @patch('app.services.post_service.AttachmentService')
    @patch('app.services.post_service.Post')
    def test_create_post_with_files(self, mock_post_class, mock_attachment_service, 
                                     sample_post_data, mock_post, mock_upload_file):
        """Test: Crear post con archivos adjuntos"""
        # Arrange
        from app.services.post_service import PostService
        from app.schemas.post_schema import PostCreate
        
        mock_post_class.return_value = mock_post
        service = PostService()
        post_data = PostCreate(**sample_post_data)
        
        # Act
        result = service.create_post("org_123", post_data, files=[mock_upload_file])
        
        # Assert
        mock_post.save.assert_called_once()
        assert result == mock_post
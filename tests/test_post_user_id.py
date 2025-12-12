from unittest.mock import Mock, patch
from app.services.post_service import PostService
from app.schemas.post_schema import PostCreate

class TestPostUserId:
    @patch('app.services.post_service.Post')
    def test_create_post_with_user_id(self, mock_post_class, sample_post_data, mock_post):
        """Test: Crear un post con user_id"""
        # Arrange
        mock_post_class.return_value = mock_post
        service = PostService()
        post_data = PostCreate(**sample_post_data)
        
        # Act
        result = service.create_post("org_123", post_data)
        
        # Assert
        # Verify that Post constructor was called with user_id
        mock_post_class.assert_called_with(
            organization_id="org_123",
            user_id="user_123",
            title="Test Post Title",
            content="This is test content for the post"
        )
        assert result.user_id == "user_123"

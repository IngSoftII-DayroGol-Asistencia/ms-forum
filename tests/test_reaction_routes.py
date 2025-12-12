"""
Tests para las rutas de reacciones (reaction_routes.py)
Verifican los endpoints de la API para likes/dislikes
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

class TestReactionRoutes:
    """Tests para las rutas de reacciones"""
    
    @patch('app.api.v1.reaction_routes.reaction_service.add_or_update_reaction')
    def test_add_like_reaction(self, mock_add_reaction, client, sample_reaction_data):
        """Test: POST /orgs/{org_id}/forum/posts/{post_id}/reactions/ - Agregar like"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        mock_add_reaction.return_value = {
            "message": "Reaction added",
            "likes_count": 1,
            "dislikes_count": 0,
            "user_reaction": "like"
        }
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/reactions/",
            json=sample_reaction_data
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Reaction added"
        assert data["likes_count"] == 1
        assert data["user_reaction"] == "like"
    
    @patch('app.api.v1.reaction_routes.reaction_service.add_or_update_reaction')
    def test_add_dislike_reaction(self, mock_add_reaction, client):
        """Test: Agregar dislike a un post"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        reaction_data = {"user_id": "user_123", "reaction_type": "dislike"}
        mock_add_reaction.return_value = {
            "message": "Reaction added",
            "likes_count": 0,
            "dislikes_count": 1,
            "user_reaction": "dislike"
        }
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/reactions/",
            json=reaction_data
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["dislikes_count"] == 1
        assert data["user_reaction"] == "dislike"
    
    @patch('app.api.v1.reaction_routes.reaction_service.add_or_update_reaction')
    def test_toggle_reaction_off(self, mock_add_reaction, client, sample_reaction_data):
        """Test: Toggle - remover reacción al hacer click de nuevo"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        mock_add_reaction.return_value = {
            "message": "Reaction removed",
            "likes_count": 0,
            "dislikes_count": 0,
            "user_reaction": None
        }
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/reactions/",
            json=sample_reaction_data
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Reaction removed"
        assert data["user_reaction"] is None
    
    @patch('app.api.v1.reaction_routes.reaction_service.add_or_update_reaction')
    def test_change_reaction_type(self, mock_add_reaction, client):
        """Test: Cambiar de like a dislike"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        reaction_data = {"user_id": "user_123", "reaction_type": "dislike"}
        mock_add_reaction.return_value = {
            "message": "Reaction updated",
            "likes_count": 0,
            "dislikes_count": 1,
            "user_reaction": "dislike"
        }
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/reactions/",
            json=reaction_data
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Reaction updated"
    
    @patch('app.api.v1.reaction_routes.reaction_service.get_reaction_stats')
    def test_get_reaction_stats(self, mock_get_stats, client):
        """Test: GET /orgs/{org_id}/forum/posts/{post_id}/reactions/stats"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        mock_get_stats.return_value = {
            "likes_count": 5,
            "dislikes_count": 2,
            "user_reaction": "like"
        }
        
        # Act
        response = client.get(
            f"/orgs/org_123/forum/posts/{post_id}/reactions/stats?user_id=user_123"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["likes_count"] == 5
        assert data["dislikes_count"] == 2
        assert data["user_reaction"] == "like"
    
    @patch('app.api.v1.reaction_routes.reaction_service.get_reaction_stats')
    def test_get_reaction_stats_no_user(self, mock_get_stats, client):
        """Test: Obtener stats sin especificar usuario"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        mock_get_stats.return_value = {
            "likes_count": 5,
            "dislikes_count": 2,
            "user_reaction": None
        }
        
        # Act
        response = client.get(
            f"/orgs/org_123/forum/posts/{post_id}/reactions/stats"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["user_reaction"] is None
    
    @patch('app.api.v1.reaction_routes.reaction_service.remove_reaction')
    def test_remove_reaction(self, mock_remove, client):
        """Test: DELETE /orgs/{org_id}/forum/posts/{post_id}/reactions/"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        mock_remove.return_value = {
            "message": "Reaction removed successfully",
            "likes_count": 4,
            "dislikes_count": 2
        }
        
        # Act
        response = client.delete(
            f"/orgs/org_123/forum/posts/{post_id}/reactions/?user_id=user_123"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Reaction removed successfully"
    
    @patch('app.api.v1.reaction_routes.reaction_service.add_or_update_reaction')
    def test_add_reaction_invalid_post(self, mock_add_reaction, client, sample_reaction_data):
        """Test: Agregar reacción a post inexistente"""
        # Arrange
        mock_add_reaction.side_effect = HTTPException(status_code=404, detail="Post not found")
        post_id = "invalid_id"
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/reactions/",
            json=sample_reaction_data
        )
        
        # Assert
        assert response.status_code == 404
    
    @patch('app.api.v1.reaction_routes.reaction_service.add_or_update_reaction')
    def test_add_reaction_invalid_type(self, mock_add_reaction, client):
        """Test: Agregar reacción con tipo inválido"""
        # Arrange
        post_id = "507f1f77bcf86cd799439011"
        invalid_data = {"user_id": "user_123", "reaction_type": "love"}
        
        # Act
        response = client.post(
            f"/orgs/org_123/forum/posts/{post_id}/reactions/",
            json=invalid_data
        )
        
        # Assert
        assert response.status_code == 422  # Validation error
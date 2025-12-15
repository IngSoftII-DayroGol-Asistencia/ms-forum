from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime
from .post_model import Post

class Reaction(Document):
    """
    Modelo para manejar likes/dislikes en posts
    Cada documento representa una reacción de un usuario a un post
    """
    post = ReferenceField(Post, required=True, reverse_delete_rule=2)  # CASCADE
    user_id = StringField(required=True, max_length=100)  # ID del usuario que reaccionó
    reaction_type = StringField(required=True, choices=['like', 'dislike'])  # tipo de reacción
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'reactions',
        'indexes': [
            'post',
            'user_id',
            ('post', 'user_id'),  # Índice compuesto para búsquedas rápidas
            'reaction_type'
        ],
        'auto_create_index': False
    }
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "post_id": str(self.post.id),
            "user_id": self.user_id,
            "reaction_type": self.reaction_type,
            "created_at": self.created_at.isoformat()
        }
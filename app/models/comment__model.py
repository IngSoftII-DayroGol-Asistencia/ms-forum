from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime
from .post_model import Post

class Comment(Document):
    post = ReferenceField(Post, required=True, reverse_delete_rule=2)  # CASCADE delete
    user_name = StringField(required=True, max_length=100)
    content = StringField(required=True, max_length=1000)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'comments',
        'indexes': [
            'post',  # Índice para buscar comentarios por post rápidamente
            '-created_at'  # Índice para ordenar por fecha
        ]
    }
    
    def to_dict(self):
        """Método helper para serializar el comentario"""
        return {
            "id": str(self.id),
            "post_id": str(self.post.id),
            "user_name": self.user_name,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }
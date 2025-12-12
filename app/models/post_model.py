from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, IntField
from datetime import datetime

class Post(Document):
    organization_id = StringField(required=True, max_length=100)
    title = StringField(required=True, max_length=200)
    content = StringField(required=True, max_length=5000)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    # Referencias a attachments
    attachments = ListField(ReferenceField('Attachment'))
    
    # Contadores para optimizar queries
    likes_count = IntField(default=0)
    dislikes_count = IntField(default=0)
    comments_count = IntField(default=0)
    
    meta = {
        'collection': 'posts',
        'indexes': [
            'organization_id',
            '-created_at',  # Para ordenar posts por fecha descendente
            ('organization_id', '-created_at')  # Índice compuesto
        ]
    }
    
    def to_dict(self):
        """Método helper para serializar el post"""
        return {
            "id": str(self.id),
            "organization_id": self.organization_id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "likes_count": self.likes_count,
            "dislikes_count": self.dislikes_count,
            "comments_count": self.comments_count,
            "attachments": [str(att.id) for att in self.attachments] if self.attachments else []
        }
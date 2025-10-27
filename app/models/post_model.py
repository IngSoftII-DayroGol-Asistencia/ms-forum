from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Post(Document):
    title = StringField(required=True, max_length=200)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

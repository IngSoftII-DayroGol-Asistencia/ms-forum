from mongoengine import Document, StringField, IntField, DateTimeField
from datetime import datetime

class Attachment(Document):
    file_name = StringField(required=True)      # nombre original
    stored_name = StringField(required=True)    # nombre con el que se guarda en disco
    content_type = StringField(required=True)   # MIME type (image/png, pdf, etc.)
    size_bytes = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)

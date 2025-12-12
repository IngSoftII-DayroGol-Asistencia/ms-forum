from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class AttachmentOut(BaseModel):
    id: str
    file_name: str
    url: str
    content_type: str
    size_bytes: int

class PostOut(PostCreate):
    id: str  
    created_at: datetime
    organization_id: str           
    attachments: List[AttachmentOut] = []

    class ConfigDict:
        from_attributes = True

    @staticmethod
    def from_orm(post):
        post_dict = post.to_mongo()
        post_dict['id'] = str(post_dict['_id'])

        # Construimos la lista de adjuntos
        attachments = []
        for att in getattr(post, "attachments", []):
            attachments.append(
                AttachmentOut(
                    id=str(att.id),
                    file_name=att.file_name,
                    content_type=att.content_type,
                    size_bytes=att.size_bytes,
                    url=f"/files/{att.stored_name}",
                )
            )

        return PostOut(
            id=post_dict['id'],
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            organization_id=post.organization_id,   
            attachments=attachments,
        )

class PostUpdate(BaseModel):
    title: Optional[str] = None  
    content: Optional[str] = None  

    class ConfigDict:
        from_attributes = True

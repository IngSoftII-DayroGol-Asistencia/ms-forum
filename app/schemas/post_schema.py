from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: str


class PostOut(PostCreate):
    id: str  
    created_at: datetime
    organization_id: str           

    class ConfigDict:
        from_attributes = True

    @staticmethod
    def from_orm(post):
        post_dict = post.to_mongo()
        post_dict['id'] = str(post_dict['_id'])

        return PostOut(
            id=post_dict['id'],
            title=post.title,
            content=post.content,
            user_id=post.user_id,
            created_at=post.created_at,
            organization_id=post.organization_id,   
        )

class PostUpdate(BaseModel):
    title: Optional[str] = None  
    content: Optional[str] = None  

    class ConfigDict:
        from_attributes = True

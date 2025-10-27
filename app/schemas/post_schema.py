from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(PostCreate):
    id: str  
    created_at: datetime

    class ConfigDict:
        orm_mode = True

    @staticmethod
    def from_orm(post):
        # Convertir ObjectId a string
        post_dict = post.to_mongo()  # Convertir el documento de Mongo a dict
        post_dict['id'] = str(post_dict['_id'])  # Convertir ObjectId a string
        return PostOut(**post_dict)

class PostUpdate(BaseModel):
    title: Optional[str] = None  
    content: Optional[str] = None  

    class ConfigDict:
        orm_mode = True
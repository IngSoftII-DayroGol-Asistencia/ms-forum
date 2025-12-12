from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    user_name: str
    content: str

class CommentOut(BaseModel):
    id: str
    post_id: str
    user_name: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
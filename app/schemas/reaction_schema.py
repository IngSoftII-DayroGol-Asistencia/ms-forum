from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class ReactionCreate(BaseModel):
    """Schema para crear una reacción"""
    user_id: str = Field(..., min_length=1, max_length=100)
    reaction_type: Literal['like', 'dislike']

class ReactionOut(BaseModel):
    """Schema para respuesta de reacción"""
    id: str
    post_id: str
    user_id: str
    reaction_type: str
    created_at: str

class ReactionStats(BaseModel):
    """Schema para estadísticas de reacciones de un post"""
    likes_count: int
    dislikes_count: int
    user_reaction: str | None = None  # 'like', 'dislike' o None
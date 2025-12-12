from fastapi import APIRouter, HTTPException
from app.schemas.comment_schema import CommentCreate, CommentOut
from app.services.comment_service import CommentService

router = APIRouter(prefix="/orgs/{org_id}/forum/posts/{post_id}/comments", tags=["Comments"])

comment_service = CommentService()

@router.post("/", status_code=201)
def create_comment(org_id: str, post_id: str, comment_data: CommentCreate):
    try:
        comment = comment_service.create_comment(
            post_id=post_id,
            user_name=comment_data.user_name,
            content=comment_data.content
        )
        
        # Serializar manualmente para evitar problemas con ReferenceField
        return {
            "id": str(comment.id),
            "post_id": str(comment.post.id),
            "user_name": comment.user_name,
            "content": comment.content,
            "created_at": comment.created_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en create_comment route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_comments(org_id: str, post_id: str):
    try:
        comments = comment_service.get_comments_for_post(post_id)
        
        # Serializar la lista de comentarios
        return [
            {
                "id": str(comment.id),
                "post_id": str(comment.post.id),
                "user_name": comment.user_name,
                "content": comment.content,
                "created_at": comment.created_at.isoformat()
            }
            for comment in comments
        ]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_comments route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{comment_id}")
def delete_comment(org_id: str, post_id: str, comment_id: str):
    try:
        return comment_service.delete_comment(comment_id)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en delete_comment route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
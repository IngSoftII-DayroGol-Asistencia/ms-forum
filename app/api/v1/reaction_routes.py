from fastapi import APIRouter, HTTPException, Query
from app.schemas.reaction_schema import ReactionCreate, ReactionStats
from app.services.reaction_service import ReactionService

router = APIRouter(prefix="/orgs/{org_id}/forum/posts/{post_id}/reactions", tags=["Reactions"])

reaction_service = ReactionService()

@router.post("/", status_code=200)
def add_reaction(org_id: str, post_id: str, reaction_data: ReactionCreate):
    """
    Agregar o actualizar una reacción (like/dislike) a un post.
    - Si el usuario no ha reaccionado, crea la reacción
    - Si el usuario ya reaccionó con el mismo tipo, la elimina (toggle)
    - Si el usuario reaccionó con otro tipo, la cambia
    """
    try:
        result = reaction_service.add_or_update_reaction(
            post_id=post_id,
            user_id=reaction_data.user_id,
            reaction_type=reaction_data.reaction_type
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en add_reaction route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=ReactionStats)
def get_reaction_stats(
    org_id: str, 
    post_id: str,
    user_id: str = Query(None, description="ID del usuario para saber su reacción")
):
    """
    Obtener estadísticas de reacciones de un post.
    Opcionalmente, incluye la reacción del usuario si se proporciona user_id.
    """
    try:
        return reaction_service.get_reaction_stats(post_id=post_id, user_id=user_id)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_reaction_stats route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
def remove_reaction(org_id: str, post_id: str, user_id: str = Query(...)):
    """
    Eliminar la reacción de un usuario a un post.
    """
    try:
        return reaction_service.remove_reaction(post_id=post_id, user_id=user_id)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en remove_reaction route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
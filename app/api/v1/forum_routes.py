from fastapi import APIRouter, HTTPException
from app.schemas.post_schema import PostCreate, PostOut, PostUpdate
from app.services.post_service import PostService
import uuid

router = APIRouter(prefix="/orgs/{org_id}/forum", tags=["Forum"])

service = PostService()



# Método para crear un post
@router.post("/", response_model=PostOut)
def create_post(
    org_id: str,
    post_data: PostCreate,
):
    """
    Crea un post en una organización.
    
    Espera un JSON con:
      - title: texto
      - content: texto
      - user_id: texto
    """
    try:
        # 1) Creamos el post asociado a la organización
        new_post = service.create_post(org_id, post_data)

        # 3) Devolvemos el post
        return PostOut.from_orm(new_post)

    except Exception as e:
        print(f"Error creating post: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Método para obtener todos los posts
@router.get("/", response_model=list[PostOut])
def get_posts(org_id: str):
    """
    Obtiene todos los posts de una organización.
    """
    posts = service.get_all_posts(org_id)
    return [PostOut.from_orm(p) for p in posts]


# Método para obtener un post por ID
@router.get("/{post_id}", response_model=PostOut)
def get_post_by_id(org_id: str, post_id: str):
    """
    Obtiene un post por id dentro de una organización.
    """
    try:
        post = service.get_post_by_id(org_id, post_id)
        return PostOut.from_orm(post)
    except Exception as e:
        print(f"Error getting post: {e}")
        raise HTTPException(status_code=404, detail=str(e))


# Método para actualizar un post
@router.put("/{post_id}", response_model=PostOut)
def update_post(org_id: str, post_id: str, post: PostUpdate):
    """
    Actualiza un post perteneciente a una organización.
    """
    try:
        updated_post = service.update_post(org_id, post_id, post)
        return PostOut.from_orm(updated_post)
    except Exception as e:
        print(f"Error updating post: {e}")
        raise HTTPException(status_code=404, detail=str(e))


# Método para eliminar un post
@router.delete("/{post_id}", response_model=dict)
def delete_post(org_id: str, post_id: str):
    """
    Elimina un post perteneciente a una organización.
    """
    return service.delete_post(org_id, post_id)




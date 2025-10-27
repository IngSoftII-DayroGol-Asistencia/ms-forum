from fastapi import APIRouter, HTTPException
from app.schemas.post_schema import PostCreate, PostOut, PostUpdate
from app.services.post_service import PostService

router = APIRouter(prefix="/forum", tags=["Forum"])
service = PostService()

@router.post("/", response_model=PostOut)
def create_post(post: PostCreate):
    try:
        new_post = service.create_post(post)
        return PostOut.from_orm(new_post)  # Usar from_orm para convertir ObjectId a string
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[PostOut])
def get_posts():
    posts = service.get_all_posts()
    return [PostOut.from_orm(post) for post in posts]  # Aplicar la conversión a todos los posts

@router.get("/{post_id}", response_model=PostOut)
def get_post_by_id(post_id: str):
    try:
        post = service.get_post_by_id(post_id)
        return PostOut.from_orm(post)  # Convertir el post a un modelo de salida
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: str, post: PostUpdate):
    try:
        # Llamamos al servicio para actualizar el post con los campos proporcionados
        updated_post = service.update_post(post_id, post)
        return PostOut.from_orm(updated_post)  # Convertir el post actualizado a la respuesta
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{post_id}", response_model=dict)
def delete_post(post_id: str):
    return service.delete_post(post_id)


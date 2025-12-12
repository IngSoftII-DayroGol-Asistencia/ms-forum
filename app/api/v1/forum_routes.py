from typing import List, Optional
import os
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.post_schema import PostCreate, PostOut, PostUpdate, AttachmentOut
from app.services.post_service import PostService
from app.services.attachment_service import AttachmentService
import uuid
from pathlib import Path

router = APIRouter(prefix="/orgs/{org_id}/forum", tags=["Forum"])

service = PostService()
attachment_service = AttachmentService()


# Método para crear un post
@router.post("/", response_model=PostOut)
def create_post(
    org_id: str,
    title: str = Form(...),
    content: str = Form(...),
    user_id: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
):
    """
    Crea un post en una organización y, opcionalmente,
    adjunta uno o varios archivos en la misma petición.
    
    Espera un multipart/form-data con:
      - title: texto
      - content: texto
      - user_id: texto
      - files: lista de archivos (opcional)
    """
    try:
        # 1) Construimos el DTO de creación con los datos del formulario
        post_data = PostCreate(title=title, content=content, user_id=user_id)

        # 2) Creamos el post asociado a la organización
        new_post = service.create_post(org_id, post_data)

        # 3) Si se enviaron archivos, los adjuntamos al post
        if files:
            for f in files:
                # Guardar el archivo de forma controlada y asociar
                attachment_service.attach_file_to_post(str(new_post.id), f)

            # Recargamos el post para que tenga la lista de attachments actualizada
            new_post.reload()

        # 4) Devolvemos el post con sus adjuntos
        return PostOut.from_orm(new_post)

    except Exception as e:
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
        raise HTTPException(status_code=404, detail=str(e))


# Método para eliminar un post
@router.delete("/{post_id}", response_model=dict)
def delete_post(org_id: str, post_id: str):
    """
    Elimina un post perteneciente a una organización.
    """
    return service.delete_post(org_id, post_id)


# Método para subir un archivo y asociarlo a un post
@router.post("/{post_id}/upload", response_model=AttachmentOut)
def upload_attachment(
    org_id: str,
    post_id: str,
    file: UploadFile = File(...),
):
    """
    Sube un archivo y lo asocia a un post de una organización.

    Aunque el AttachmentService no usa org_id, aquí validamos primero
    que el post realmente pertenece a la organización indicada,
    usando PostService.get_post_by_id(org_id, post_id).
    """
    try:
        # 1) Validar que el post pertenece a esa organización 
        service.get_post_by_id(org_id, post_id)

        # 2) Adjuntar archivo al post
        att = attachment_service.attach_file_to_post(post_id, file)

        # 3) Devolver metadatos del adjunto
        return AttachmentOut(
            id=str(att.id),
            file_name=att.file_name,
            content_type=att.content_type,
            size_bytes=att.size_bytes,
            url=f"/files/{att.stored_name}",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

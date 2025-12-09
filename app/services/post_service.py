from bson import ObjectId
from app.models.post_model import Post
from app.schemas.post_schema import PostCreate, PostUpdate
from app.services.attachment_service import AttachmentService
from fastapi import UploadFile  
from typing import Optional, List  

class PostService:
    def create_post(self, org_id: str, post_data: PostCreate, files: Optional[List[UploadFile]] = None) -> Post:
        post = Post(
            organization_id=org_id,
            title=post_data.title,
            content=post_data.content
        )
        post.save()  # Guardamos el post en la base de datos

        # Si se recibieron archivos, los asociamos al post
        if files:
            attachment_service = AttachmentService()  # Creamos el servicio de adjuntos
            for file in files:
                attachment_service.attach_file_to_post(str(post.id), file)  # Asociamos el archivo al post

        return post

    def get_all_posts(self, org_id: str):
        return Post.objects(organization_id=org_id).all()  

    def get_post_by_id(self, org_id: str, post_id: str) -> Post:
        post = Post.objects(
            id=ObjectId(post_id),
            organization_id=org_id           
        ).first()
        if not post:
            raise Exception("Post not found")
        return post

    def update_post(self, org_id: str, post_id: str, post_data: PostUpdate) -> Post:
        post = self.get_post_by_id(org_id, post_id)  # Filtramos por org_id y post_id
        if post_data.title:
            post.update(set__title=post_data.title)
        if post_data.content:
            post.update(set__content=post_data.content)
        post.reload()  # Recargamos el post con la nueva información
        return post

    def delete_post(self, org_id: str, post_id: str):
        post = self.get_post_by_id(org_id, post_id)
        post.delete()  # Eliminamos el post de la base de datos
        return {"message": "Post deleted successfully"}

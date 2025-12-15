from bson import ObjectId
from bson.errors import InvalidId
from app.models.post_model import Post
from app.schemas.post_schema import PostCreate, PostUpdate
from app.schemas.post_schema import PostCreate, PostUpdate
from typing import Optional  

class PostService:
    def create_post(self, org_id: str, post_data: PostCreate) -> Post:
        post = Post(
            organization_id=org_id,
            user_id=post_data.user_id,
            title=post_data.title,
            content=post_data.content
        )
        post.save()  # Guardamos el post en la base de datos
        return post

    def get_all_posts(self, org_id: str):
        return Post.objects(organization_id=org_id).all()  

    def get_post_by_id(self, org_id: str, post_id: str) -> Post:
        try:
            obj_id = ObjectId(post_id)
        except InvalidId:
            raise Exception("Invalid post ID format")

        post = Post.objects(
            id=obj_id,
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

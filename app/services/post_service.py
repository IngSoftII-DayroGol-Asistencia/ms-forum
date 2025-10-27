from bson import ObjectId
from app.models.post_model import Post
from app.schemas.post_schema import PostCreate, PostUpdate

class PostService:
    def create_post(self, post_data: PostCreate) -> Post:
        post = Post(title=post_data.title, content=post_data.content)
        post.save()
        return post

    def get_all_posts(self):
        return Post.objects.all()

    def delete_post(self, post_id: str):
        post = Post.objects(id=post_id).first()  # Buscar el post por ID
        if post:
            post.delete()  # Eliminar el post si existe
            return {"message": "Post deleted successfully"}
        else:
            raise Exception("Post not found")
    
    def get_post_by_id(self, post_id: str) -> Post:
        # Convertir el post_id a ObjectId
        post = Post.objects(id=ObjectId(post_id)).first()
        
        # Si el post no existe, lanzamos una excepción
        if not post:
            raise Exception("Post not found")
        
        return post
    
    def update_post(self, post_id: str, post_data: PostUpdate) -> Post:
            # Buscar el post por ID
            post = Post.objects(id=ObjectId(post_id)).first()
            
            # Si el post no existe, lanzamos un error
            if not post:
                raise Exception("Post not found")
            
            # Solo actualizamos los campos que fueron proporcionados
            if post_data.title:
                post.update(set__title=post_data.title)
            if post_data.content:
                post.update(set__content=post_data.content)
            
            # Recargamos el post actualizado
            post.reload()
            
            return post
from fastapi import HTTPException
from app.models.comment__model import Comment
from app.models.post_model import Post
from bson import ObjectId
from bson.errors import InvalidId

class CommentService:
    def create_comment(self, post_id: str, user_name: str, content: str) -> Comment:
        try:
            # Validar que el post_id sea un ObjectId válido
            try:
                post_object_id = ObjectId(post_id)
            except (InvalidId, TypeError):
                raise HTTPException(status_code=400, detail="Invalid post ID format")
            
            # Buscar el post al que se agregará el comentario
            post = Post.objects(id=post_object_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Crear el comentario con la REFERENCIA al post
            comment = Comment(
                post=post,  # ✅ Pasamos el objeto Post completo
                user_name=user_name,
                content=content
            )
            comment.save()
            
            # Incrementar el contador de comentarios en el post
            post.update(inc__comments_count=1)
            
            return comment
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error en create_comment: {str(e)}")  # Para debug
            raise HTTPException(status_code=500, detail=f"Error creando el comentario: {str(e)}")

    def get_comments_for_post(self, post_id: str):
        try:
            # Validar el post_id
            try:
                post_object_id = ObjectId(post_id)
            except (InvalidId, TypeError):
                raise HTTPException(status_code=400, detail="Invalid post ID format")
            
            # Primero obtenemos el post
            post = Post.objects(id=post_object_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            
            # Obtenemos todos los comentarios que referencian a ese post
            comments = Comment.objects(post=post)
            return list(comments)
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error en get_comments_for_post: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error obteniendo los comentarios: {str(e)}")

    def delete_comment(self, comment_id: str):
        try:
            # Validar el comment_id
            try:
                comment_object_id = ObjectId(comment_id)
            except (InvalidId, TypeError):
                raise HTTPException(status_code=400, detail="Invalid comment ID format")
            
            # Buscar el comentario por su ID
            comment = Comment.objects(id=comment_object_id).first()
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            
            # Decrementar el contador de comentarios en el post
            post = comment.post
            post.update(dec__comments_count=1)
            
            comment.delete()
            return {"message": "Comment deleted successfully"}
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error en delete_comment: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error eliminando el comentario: {str(e)}")
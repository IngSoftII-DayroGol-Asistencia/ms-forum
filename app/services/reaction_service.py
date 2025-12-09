from fastapi import HTTPException
from app.models.reaction_model import Reaction
from app.models.post_model import Post
from bson import ObjectId
from bson.errors import InvalidId

class ReactionService:
    
    def add_or_update_reaction(self, post_id: str, user_id: str, reaction_type: str):
        """
        Agrega o actualiza una reacción de un usuario a un post.
        Si el usuario ya reaccionó, actualiza la reacción.
        Si la nueva reacción es igual a la anterior, la elimina (toggle).
        """
        try:
            # Validar post_id
            try:
                post_object_id = ObjectId(post_id)
            except (InvalidId, TypeError):
                raise HTTPException(status_code=400, detail="Invalid post ID format")
            
            # Verificar que el post existe
            post = Post.objects(id=post_object_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            
            # Buscar si el usuario ya reaccionó a este post
            existing_reaction = Reaction.objects(post=post, user_id=user_id).first()
            
            if existing_reaction:
                # Si la reacción es la misma, la eliminamos (toggle off)
                if existing_reaction.reaction_type == reaction_type:
                    old_type = existing_reaction.reaction_type
                    existing_reaction.delete()
                    
                    # Actualizar contador en el post
                    if old_type == 'like':
                        post.update(dec__likes_count=1)
                    else:
                        post.update(dec__dislikes_count=1)
                    
                    post.reload()
                    return {
                        "message": "Reaction removed",
                        "likes_count": post.likes_count,
                        "dislikes_count": post.dislikes_count,
                        "user_reaction": None
                    }
                else:
                    # Cambiar de like a dislike o viceversa
                    old_type = existing_reaction.reaction_type
                    existing_reaction.update(set__reaction_type=reaction_type)
                    
                    # Actualizar contadores
                    if old_type == 'like':
                        post.update(dec__likes_count=1, inc__dislikes_count=1)
                    else:
                        post.update(inc__likes_count=1, dec__dislikes_count=1)
                    
                    post.reload()
                    return {
                        "message": "Reaction updated",
                        "likes_count": post.likes_count,
                        "dislikes_count": post.dislikes_count,
                        "user_reaction": reaction_type
                    }
            else:
                # Crear nueva reacción
                reaction = Reaction(
                    post=post,
                    user_id=user_id,
                    reaction_type=reaction_type
                )
                reaction.save()
                
                # Actualizar contador en el post
                if reaction_type == 'like':
                    post.update(inc__likes_count=1)
                else:
                    post.update(inc__dislikes_count=1)
                
                post.reload()
                return {
                    "message": "Reaction added",
                    "likes_count": post.likes_count,
                    "dislikes_count": post.dislikes_count,
                    "user_reaction": reaction_type
                }
                
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error en add_or_update_reaction: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing reaction: {str(e)}")
    
    def get_reaction_stats(self, post_id: str, user_id: str = None):
        """
        Obtiene las estadísticas de reacciones de un post.
        Si se proporciona user_id, también indica qué reacción tiene ese usuario.
        """
        try:
            # Validar post_id
            try:
                post_object_id = ObjectId(post_id)
            except (InvalidId, TypeError):
                raise HTTPException(status_code=400, detail="Invalid post ID format")
            
            # Verificar que el post existe
            post = Post.objects(id=post_object_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            
            # Buscar la reacción del usuario si se proporciona user_id
            user_reaction = None
            if user_id:
                reaction = Reaction.objects(post=post, user_id=user_id).first()
                if reaction:
                    user_reaction = reaction.reaction_type
            
            return {
                "likes_count": post.likes_count,
                "dislikes_count": post.dislikes_count,
                "user_reaction": user_reaction
            }
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error en get_reaction_stats: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error getting reaction stats: {str(e)}")
    
    def remove_reaction(self, post_id: str, user_id: str):
        """Elimina la reacción de un usuario a un post"""
        try:
            # Validar post_id
            try:
                post_object_id = ObjectId(post_id)
            except (InvalidId, TypeError):
                raise HTTPException(status_code=400, detail="Invalid post ID format")
            
            # Verificar que el post existe
            post = Post.objects(id=post_object_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            
            # Buscar la reacción del usuario
            reaction = Reaction.objects(post=post, user_id=user_id).first()
            if not reaction:
                raise HTTPException(status_code=404, detail="Reaction not found")
            
            # Actualizar contador antes de eliminar
            if reaction.reaction_type == 'like':
                post.update(dec__likes_count=1)
            else:
                post.update(dec__dislikes_count=1)
            
            reaction.delete()
            post.reload()
            
            return {
                "message": "Reaction removed successfully",
                "likes_count": post.likes_count,
                "dislikes_count": post.dislikes_count
            }
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error en remove_reaction: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error removing reaction: {str(e)}")
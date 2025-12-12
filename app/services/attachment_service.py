import os
import uuid
from fastapi import UploadFile
from app.models.attachment_model import Attachment
from app.models.post_model import Post
from pathlib import Path
import shutil

UPLOAD_DIR = "uploads"  # Directorio donde se guardarán los archivos

class AttachmentService:
    def __init__(self, upload_dir: str = UPLOAD_DIR):
        self.upload_dir = Path(upload_dir)  
        self.upload_dir.mkdir(parents=True, exist_ok=True)  # Creamos el directorio si no existe

    def attach_file_to_post(self, post_id: str, file: UploadFile) -> Attachment:
        # 1. Buscar post
        post = Post.objects(id=post_id).first()
        if not post:
            raise Exception("Post not found")

        # 2. Generar un nombre único para el archivo
        extension = file.filename.split(".")[-1]
        stored_name = f"{uuid.uuid4()}.{extension}"  # Nombre único para el archivo
        file_path = self.upload_dir / stored_name  # Ruta donde se almacenará el archivo

        # 3. Guardar el archivo en el sistema de archivos
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)  # Guardar el buffer del archivo en el sistema de archivos

        # 4. Crear un attachment y guardarlo en la base de datos
        attachment = Attachment(
            file_name=file.filename,  # Nombre original del archivo
            stored_name=stored_name,  # Nombre con el que se guarda en el servidor
            content_type=file.content_type,  # MIME type del archivo
            size_bytes=os.path.getsize(file_path)  # Tamaño del archivo en bytes
        )
        attachment.save()  # Guardar en MongoDB

        # 5. Asociar el attachment al post
        post.update(push__attachments=attachment)  # Asociar al post
        post.reload()  # Recargar el post con el attachment

        return attachment

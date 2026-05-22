import os
import uuid

from fastapi import UploadFile

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp"
}

UPLOAD_DIR = "media/posts"


async def save_post_image(file: UploadFile) -> str:
    content_type = file.content_type

    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError("Unsupported image type")

    extension = ALLOWED_IMAGE_TYPES[content_type]

    filename = f"{uuid.uuid4().hex}{extension}"

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return f"/media/posts/{filename}"


# просмотр файла по адресу /api/v1/.....

from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    File,
    Form,
    Body
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exception_handler import handle_exception
from src.dependencies.database import get_db
from src.domain.auth_service import AuthService
from src.domain.post_service import PostService
from src.schemas.post_schema import (
    PostCreateSchema,
    PostResponseSchema,
    PostUpdateSchema
)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponseSchema])
async def get_posts(db: AsyncSession = Depends(get_db)):
    try:
        return await PostService(db).get_posts()
    except Exception as ex:
        handle_exception(ex)


@router.get("/{post_id}", response_model=PostResponseSchema)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await PostService(db).get_post(post_id)
    except Exception as ex:
        handle_exception(ex)


@router.post(
    "/",
    response_model=PostResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    title: str = Form(...),
    text: str = Form(...),
    is_published: bool = Form(True),
    location_id: int | None = Form(None),
    category_id: int | None = Form(None),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        image_path = None

        if image:
            from src.utils.file_upload import save_post_image
            image_path = await save_post_image(image)

        if category_id == 0:
            category_id = None

        if location_id == 0:
            location_id = None

        data = {
            "title": title,
            "text": text,
            "is_published": is_published,
            "location_id": location_id,
            "category_id": category_id,
            "image": image_path
        }
        validated = PostCreateSchema(**data)

        return await PostService(db).create_post(
            validated.model_dump(),
            current_user,
        )

    except Exception as ex:
        handle_exception(ex)


@router.put("/{post_id}", response_model=PostResponseSchema)
async def update_post(
    post_id: int,
    title: str | None = Form(None),
    text: str | None = Form(None),
    is_published: bool | None = Form(None),
    location_id: int | None = Form(None),
    category_id: int | None = Form(None),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        image_path = None

        if image:
            from src.utils.file_upload import save_post_image
            image_path = await save_post_image(image)

        if category_id == 0:
            category_id = None

        if location_id == 0:
            location_id = None
        
        data = {
            "title": title,
            "text": text,
            "is_published": is_published,
            "location_id": location_id,
            "category_id": category_id,
        }
        validated = PostUpdateSchema(**data)

        if image_path:
            data["image"] = image_path

        return await PostService(db).update_post(
            post_id,
            validated.model_dump(),
            current_user=current_user,
        )

    except Exception as ex:
        handle_exception(ex)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        await PostService(db).delete_post(post_id, current_user=current_user)

    except Exception as ex:
        handle_exception(ex)


@router.post("/{post_id}/reaction", response_model=PostResponseSchema)
async def react_to_post(
    post_id: int,
    value: int = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        return await PostService(db).react_to_post(
            post_id,
            value,
            current_user
        )

    except Exception as ex:
        handle_exception(ex)

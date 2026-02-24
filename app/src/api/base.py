from fastapi import APIRouter, HTTPException
from typing import List

from ..models.blogicum_models import Post
from ..schemas.blogicum_schemas import PostSchema

router = APIRouter(prefix="/posts", tags=["Posts"])

fake_posts_db: List[Post] = []
post_counter = 1


@router.get("/", response_model=List[PostSchema])
def get_posts():
    return fake_posts_db


@router.get("/{post_id}", response_model=PostSchema)
def get_post(post_id: int):
    for post in fake_posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")


@router.post("/", response_model=PostSchema, status_code=201)
def create_post(data: PostSchema):
    global post_counter
    post = Post(**data.dict())
    post.id = post_counter
    post_counter += 1

    fake_posts_db.append(post)
    return post


@router.put("/{post_id}", response_model=PostSchema)
def update_post(post_id: int, data: PostSchema):
    for post in fake_posts_db:
        if post.id == post_id:
            post.title = data.title
            post.text = data.text
            post.pub_date = data.pub_date
            post.author_id = data.author_id
            post.location_id = data.location_id
            post.category_id = data.category_id
            post.image = data.image
            return post

    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int):
    global fake_posts_db
    for post in fake_posts_db:
        if post.id == post_id:
            fake_posts_db = [p for p in fake_posts_db if p.id != post_id]
            return

    raise HTTPException(status_code=404, detail="Post not found")

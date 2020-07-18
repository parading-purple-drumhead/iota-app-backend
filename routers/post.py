from fastapi import APIRouter, HTTPException
from models import Post
from typing import Dict
from routers import db
from datetime import datetime
from pytz import timezone

router = APIRouter()


@router.get("", response_model=Dict[str, Post])
def get_all_posts():
    try:
        posts_ref = db.collection(u"posts").stream()
        data = {}
        for post in posts_ref:
            data[post.id] = post.to_dict()
        return data

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{post_id}", response_model=Post)
def get_post(post_id):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        return post

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add")
def add_post(post: Post):
    try:
        doc_ref = db.collection(u"posts")
        doc_ref.add(dict(post))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{post_id}")
def edit_post(post_id, post: Post):
    try:
        edit = db.collection(u"posts").document(post_id)
        new_data = post.dict(exclude_none=True, exclude_defaults=True)

        if "created_at" or "updated_at" in new_data:
            raise Exception()

        new_data["updated_at"] = datetime.now(timezone("Asia/Kolkata"))

        edit.update(new_data)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}")
def delete_post(post_id):
    try:
        db.collection(u"posts").document(post_id).delete()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{post_id}/comment")
def post_comment(post_id, post: Post):
    try:
        edit = db.collection(u"posts").document(post_id)
        new_data = post.dict(exclude_none=True, exclude_defaults=True)

        edit.update(new_data)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

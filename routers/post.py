from fastapi import APIRouter, HTTPException, Request
from models import Post, Comment
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
def add_post(post: Post, request: Request):
    try:
        uid = request.headers.get("uid")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"] == True:
            doc_ref = db.collection(u"posts")
            doc_ref.add(dict(post))
        raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{post_id}")
def edit_post(post_id, post: Post, request: Request):
    try:
        uid = request.headers.get("uid")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"] == True:
            edit = db.collection(u"posts").document(post_id)
            new_data = post.dict(exclude_none=True, exclude_defaults=True)

            if "created_at" in new_data or "updated_at" in new_data:
                raise Exception()

            new_data["updated_at"] = datetime.now(timezone("Asia/Kolkata"))

            edit.update(dict(new_data))
        raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}")
def delete_post(post_id, request: Request):
    try:
        uid = request.headers.get("uid")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"] == True:
            db.collection(u"posts").document(post_id).delete()
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{post_id}/comment")
def add_comment(post_id, comment: Comment):
    try:
        doc_ref = db.collection(u"posts")
        doc = doc_ref.document(post_id).collection(u"comments")

        doc.add(dict(comment))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{post_id}/comment/{comment_id}")
def edit_comment(post_id, comment_id, comment: Comment, request: Request):
    try:
        doc_ref = db.collection(u"posts").document(post_id)
        doc = doc_ref.collection(u"comment").document(comment_id)
        doc_get = doc.get().to_dict()
        uid = request.headers.get("uid")
        if doc_get["user_id"] == uid:
            new_data = comment.dict(exclude_none=True, exclude_defaults=True)
            doc.update(new_data)
        else:
            raise Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}/comment/{comment_id}")
def delete_comment(post_id, comment_id, request: Request):
    try:
        doc_ref = db.collection(u"posts").document(post_id)
        doc = doc_ref.collection(u"comment").document(comment_id)
        doc_get = doc.get().to_dict()
        uid = request.headers.get("uid")
        if doc_get["user_id"] == uid:
            doc.delete()
        else:
            raise Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

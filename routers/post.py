from fastapi import APIRouter, HTTPException
from models import Post, Question
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

        if "created_at" in new_data or "updated_at" in new_data:
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


@router.post("/{post_id}/question")
def add_question(post_id, question: Question):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id).collection(u"questions")
            doc.add(dict(question))

        else:
            return Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{post_id}/question", response_model=Dict[str, Question])
def get_all_question(post_id):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id)
            question_ref = doc.collection("questions").stream()
            data = {}
            for question in question_ref:
                data[question.id] = question.to_dict()
            return data
        else:
            return Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}/question/{question_id}")
def delete_question(question_id, post_id):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id)
            doc.collection("questions").document(question_id).delete()
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{post_id}/question/{question_id}")
def edit_question(post_id, question_id, question: Question):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id)
            doc_ref = doc.collection("questions").document(question_id)
            new_data = question.dict(exclude_none=True, exclude_defaults=True)
            doc_ref.update(new_data)
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

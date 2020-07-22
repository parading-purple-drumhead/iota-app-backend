from fastapi import APIRouter, HTTPException, Request
from models import Post, Comment, Question, Quiz, QuestionA
from typing import Dict
from routers import db
from datetime import datetime
from pytz import timezone
import random

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
        if doc["admin"]:
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
        if doc["admin"]:
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
        if doc["admin"]:
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


@router.post("/{post_id}/submit")
def submint_quiz(post_id, quiz: Quiz):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id)
            doc_ref = doc.collection("questions").document(quiz.question_id).get().to_dict()
            print(doc_ref["answer"][0])
            print(quiz.answer)
            if doc_ref["answer"][0] == quiz.answer:
                return {
                    "mark": "1"
                }
            else:
                return {
                    "mark": "0"
                }
        else:
            return Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{post_id}/random", response_model=Dict[str, QuestionA])
def get_random_question(post_id):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id)
            question_ref = doc.collection("questions").order_by("number").limit(3).stream()
            data = {}
            for question in question_ref:
                data[question.id] = question.to_dict()
                d = db.collection(u"questionbank").document(post_id)
                edit = d.collection(u"questions").document(question.id)
                edit.update({u"number": random.randint(1, 100)})
            return data
        else:
            return Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

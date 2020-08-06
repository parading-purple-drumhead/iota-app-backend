from fastapi import APIRouter, HTTPException, Request
from typing import Dict, List
from models import Post, Comment, Question, Quiz
from firebase_admin import firestore
from routers import db
from datetime import datetime
from pytz import timezone
import random

router = APIRouter()


@router.get("", response_model=Dict[str, Post])
def get_all_posts():
    try:
        posts_ref = db.collection(u"posts").get()
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
        post_ref = db.collection(u"posts").document(post_id)
        post = post_ref.get().to_dict()
        comments_ref = post_ref.collection(u"comments").get()
        post["comments"] = []
        for comment in comments_ref:
            comment_dict = comment.to_dict()
            comment_dict["id"] = comment.id
            post["comments"].append(comment_dict)
        return post

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add")
def add_post(post: Post, request: Request):
    try:
        uid = request.headers.get("uid")
        course_id = request.headers.get("course_id")
        chapter_id = request.headers.get("chapter_id")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            doc_ref = db.collection(u"posts")
            docref = doc_ref.add(dict(post))
            course_ref = db.collection(u"courses").document(course_id)
            chapter_ref = course_ref.collection("chapters").document(chapter_id)
            chapter_ref.update({
                u"post_ids": firestore.ArrayUnion([docref[1].id])
            })

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
        course_id = request.headers.get("course_id")
        chapter_id = request.headers.get("chapter_id")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            db.collection(u"posts").document(post_id).delete()
            course_ref = db.collection(u"courses").document(course_id)
            course_ref.collection(u"chapters").document(chapter_id).update({
                u"post_ids": firestore.ArrayRemove([post_id])
            })
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
        doc = doc_ref.collection(u"comments").document(comment_id)
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
        doc = doc_ref.collection(u"comments").document(comment_id)
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
def submit_quiz(post_id, quiz: List[Quiz]):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            mark = 0
            for i in range(len(quiz)):
                if quiz[i].answer[0] == quiz[i].response:
                    mark = mark + 1

            return {
                "mark": mark
                }
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{post_id}/random")
def get_random_question(post_id):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id)
            question_ref = doc.collection("questions").order_by("number").limit(6).stream()
            data = [None] * 6
            i = 0
            for question in question_ref:
                editing = doc.collection(u"questions").document(question.id)
                editing.update({u"number": random.randint(1, 100)})
                data[i] = question.to_dict()
                i = i + 1
            return data
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

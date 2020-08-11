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
        posts_ref = db.collection(u"posts").stream()
        data = {}
        for post in posts_ref:
            data[post.id] = post.to_dict()
        return data

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{post_id}")
def get_post(post_id, request: Request):
    try:
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id)
            random_ref = doc.collection(u"questions")
            i = 0
            data = {}
            easy = random_ref.where(u"difficulty", u"==", u"easy")
            easy_ref = easy.order_by("number").limit(2).stream()
            for info in easy_ref:
                info_dict = info.to_dict()
                del info_dict["answer"]
                del info_dict["difficulty"]
                del info_dict["number"]
                data[info.id] = info_dict
                edit = doc.collection(u"questions").document(info.id)
                edit.update({u"number": random.randint(1, 100)})
                i = i + 1

            medium = random_ref.where(u"difficulty", u"==", u"medium")
            medium_ref = medium.order_by("number").limit(2).stream()
            for info in medium_ref:
                info_dict = info.to_dict()
                del info_dict["answer"]
                del info_dict["difficulty"]
                del info_dict["number"]
                data[info.id] = info_dict
                edit = doc.collection(u"questions").document(info.id)
                edit.update({u"number": random.randint(1, 100)})
                i = i + 1

            hard = random_ref.where(u"difficulty", u"==", u"hard")
            hard_ref = hard.order_by("number").limit(2).stream()
            for info in hard_ref:
                info_dict = info.to_dict()
                del info_dict["answer"]
                del info_dict["difficulty"]
                del info_dict["number"]
                data[info.id] = info_dict
                edit = doc.collection(u"questions").document(info.id)
                edit.update({u"number": random.randint(1, 100)})
                i = i + 1

            return data

        else:
            post_ref = db.collection(u"posts").document(post_id)
            post = post_ref.get().to_dict()
            comments_ref = post_ref.collection(u"comments").get()
            post["comments"] = []
            for comment in comments_ref:
                comment_dict = comment.to_dict()
                user = db.collection(u"users").document(comment_dict["user_id"]).get().to_dict()
                comment_dict["user_name"] = user["name"]
                comment_dict["user_avatar"] = user["avatar"]
                comment_dict["id"] = comment.id
                post["comments"].append(comment_dict)
            return post

        raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add")
def add_post(post: Post, request: Request):
    try:
        uid = request.headers.get("uid")
        chapter_id = request.headers.get("chapter_id")
        course_id = request.headers.get("course_id")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            doc_ref = db.collection(u"posts")
            docref = doc_ref.add(dict(post))
            chapter_ref = db.collection("courses").document(course_id)
            chap = chapter_ref.collection("chapters").document(chapter_id)
            chap.set({
                u"post_ids": firestore.ArrayUnion([docref[1].id])
            }, merge=True)

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
        chapter_id = request.headers.get("chapter_id")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            db.collection(u"posts").document(post_id).delete()
            db.collection(u"chapters").document(chapter_id).update({
                u"posts": firestore.ArrayRemove([post_id])
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

        raise Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{post_id}/question")
def add_question(post_id, question: Question, request: Request):
    try:
        uid = request.headers.get("uid")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            post = db.collection(u"posts").document(post_id).get().to_dict()
            if post["type"] == "quiz":
                doc_ref = db.collection(u"questionbank").document(post_id)
                doc1 = doc_ref.collection(u"questions")
                doc1.add(dict(question))
            else:
                raise Exception()

        else:
            raise Exception()

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
def delete_question(question_id, post_id, request: Request):
    try:
        uid = request.headers.get("uid")
        doc1 = db.collection(u"users").document(uid).get().to_dict()
        if doc1["admin"]:
            post = db.collection(u"posts").document(post_id).get().to_dict()
            if post["type"] == "quiz":
                doc = db.collection(u"questionbank").document(post_id)
                doc.collection("questions").document(question_id).delete()
            else:
                raise Exception()
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{post_id}/question/{question_id}")
def edit_question(post_id, question_id, question: Question, request: Request):
    try:
        uid = request.headers.get("uid")
        doc1 = db.collection(u"users").document(uid).get().to_dict()
        if doc1["admin"]:
            post = db.collection(u"posts").document(post_id).get().to_dict()
            if post["type"] == "quiz":
                doc = db.collection(u"questionbank").document(post_id)
                doc_ref = doc.collection("questions").document(question_id)
                new = question.dict(exclude_none=True, exclude_defaults=True)
                doc_ref.update(new)
            else:
                raise Exception()
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{post_id}/submit")
def submit_quiz(post_id, quiz: List[Quiz], request: Request):
    try:
        result = {}
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id)
            mark = 0
            for i in range(len(quiz)):
                result.update({quiz[i].question_id: quiz[i].answer})
                doc_ref = doc.collection("questions").document(quiz[i].question_id).get().to_dict()
                if doc_ref["answer"][0] == quiz[i].answer:
                    mark += 1

            uid = request.headers.get("uid")
            user = db.collection(u"users").document(uid)
            user.update({
                u"points": firestore.Increment(mark)
            })

            result.update({"mark": mark})
            return result

        else:
            return Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

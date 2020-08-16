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
        user = db.collection(u"users").document(uid).get().to_dict()
        if user["admin"]:
            posts_ref = db.collection(u"posts")
            post.created_at = datetime.now()
            post_ref = posts_ref.add(dict(post))
            course_ref = db.collection("courses").document(course_id)
            chapter = course_ref.collection("chapters").document(chapter_id)
            chapter.update({
                u"post_ids": firestore.ArrayUnion([post_ref[1].id])
            })

        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{post_id}")
def edit_post(post_id, post: Post, request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid).get().to_dict()
        if user["admin"]:
            post_ref = db.collection(u"posts").document(post_id)
            new_data = post.dict(exclude_none=True, exclude_defaults=True)

            if "created_at" in new_data or "updated_at" in new_data:
                raise Exception()

            new_data["updated_at"] = datetime.now(timezone("Asia/Kolkata"))

            post_ref.update(dict(new_data))
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}")
def delete_post(post_id, request: Request):
    try:
        uid = request.headers.get("uid")
        chapter_id = request.headers.get("chapter_id")
        course_id = request.headers.get("course_id")
        user = db.collection(u"users").document(uid).get().to_dict()
        if user["admin"]:
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


@router.get("/{post_id}/comment")
def get_comment(post_id):
    try:
        post_ref = db.collection(u"posts").document(post_id).collection(u"comments")
        comment_ref = post_ref.order_by(u"created_at", direction=firestore.Query.DESCENDING).get()
        comments = []
        for comment in comment_ref:
            comment_dict = comment.to_dict()
            user = db.collection(u"users").document(comment_dict["user_id"]).get().to_dict()
            comment_dict["user_name"] = user["name"]
            comment_dict["user_avatar"] = user["avatar"]
            comment_dict["id"] = comment.id
            comments.append(comment_dict)
        return comments

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{post_id}/comment")
def add_comment(post_id, comment: Comment, request: Request):
    try:
        doc_ref = db.collection(u"posts")
        doc = doc_ref.document(post_id).collection(u"comments")
        comment.created_at = datetime.now()
        comment.user_id = request.headers.get("uid")
        doc.add(dict(comment))
        comments = []
        comments_ref = doc.order_by(u"created_at", direction=firestore.Query.DESCENDING).get()
        for comment in comments_ref:
            comment_dict = comment.to_dict()
            user = db.collection(u"users").document(comment_dict["user_id"]).get().to_dict()
            comment_dict["user_name"] = user["name"]
            comment_dict["user_avatar"] = user["avatar"]
            comment_dict["id"] = comment.id
            comments.append(comment_dict)
        return comments

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{post_id}/comment/{comment_id}")
def edit_comment(post_id, comment_id, comment: Comment, request: Request):
    try:
        post_ref = db.collection(u"posts").document(post_id)
        comment_ref = post_ref.collection(u"comments").document(comment_id)
        comment_get = comment_ref.get().to_dict()
        uid = request.headers.get("uid")
        if comment_get["user_id"] == uid:
            new_data = comment.dict(exclude_none=True, exclude_defaults=True)
            comment_ref.update(new_data)

        else:
            raise Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}/comment/{comment_id}")
def delete_comment(post_id, comment_id, request: Request):
    try:
        post_ref = db.collection(u"posts").document(post_id)
        comment_ref = post_ref.collection(u"comments").document(comment_id)
        comment_get = comment_ref.get().to_dict()
        uid = request.headers.get("uid")
        if comment_get["user_id"] == uid:
            comment_ref.delete()

        else:
            raise Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{post_id}/question")
def add_question(post_id, question: Question, request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid).get().to_dict()
        if user["admin"]:
            post = db.collection(u"posts").document(post_id).get().to_dict()
            if post["type"] == "quiz":
                ques_postid = db.collection(u"questionbank").document(post_id)
                question_ref = ques_postid.collection(u"questions")
                question_ref.add(dict(question))
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
            ques_postid = db.collection(u"questionbank").document(post_id)
            question_ref = ques_postid.collection("questions").stream()
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
        user = db.collection(u"users").document(uid).get().to_dict()
        if user["admin"]:
            post = db.collection(u"posts").document(post_id).get().to_dict()
            if post["type"] == "quiz":
                ques_postid = db.collection(u"questionbank").document(post_id)
                ques_postid.collection("questions").document(question_id).delete()
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
        user = db.collection(u"users").document(uid).get().to_dict()
        if user["admin"]:
            post = db.collection(u"posts").document(post_id).get().to_dict()
            if post["type"] == "quiz":
                ques_postid = db.collection(u"questionbank").document(post_id)
                question_ref = ques_postid.collection("questions").document(question_id)
                new = question.dict(exclude_none=True, exclude_defaults=True)
                question_ref.update(new)
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
        result = []
        results = {}
        post = db.collection(u"posts").document(post_id).get().to_dict()
        if post["type"] == "quiz":
            doc = db.collection(u"questionbank").document(post_id)
            mark = 0
            for i in range(len(quiz)):
                doc_ref = doc.collection("questions").document(quiz[i].question_id).get().to_dict()
                result.append({"question_id": quiz[i].question_id, "answer": doc_ref["answer"][0]})
                if doc_ref["answer"][0] == quiz[i].answer:
                    mark += 1

            results.update({"response": result})
            uid = request.headers.get("uid")
            user = db.collection(u"users").document(uid)
            user.update({
                u"points": firestore.Increment(mark)
            })

            results.update({"mark": mark})
            return results

        else:
            return Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

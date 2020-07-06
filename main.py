import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from fastapi import FastAPI
import datetime
import models

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI()


@app.post("/addPost")
def addPost(post: models.post):
    try:
        doc_ref = db.collection(u"posts")
        data = {
            u"title": post.title,
            u"type": post.post_type,
            u"created_at": datetime.datetime.now(),
            u"updated_at": datetime.datetime.now(),
        }

        if post.post_type == "video":
            data.update({
                u"description": post.description,
                u"url": post.url,
                u"resource_url": post.resource_url,
            })

        elif post.post_type == "article":
            data.update({
                u"content": post.content,
                u"resource_url": post.resource_url,
            })

        elif post.post_type == "quiz":
            data.update({
                u"questions": post.questions,
            })

        doc_ref.add(data)

        return {
            "status": True
        }

    except Exception as e:
        print(e)
        return {
            "status": False,
            "error": e
        }


@app.post("/editPost")
def editPost(post: models.post):
    try:
        edit = db.collection(u'posts').document(post.document)
        edit.update({u'title': post.title})
        edit.update({u'updated_at': firestore.SERVER_TIMESTAMP})

        if post.post_type == "video":

            edit.update({u'description': post.description})
            edit.update({u'resource_url': post.resource_url})
            edit.update({u'url': post.url})

        elif post.post_type == "article":

            edit.update({u'content': post.content})
            edit.update({u'resource_url': post.resource_url})

        else:
            edit.update({u'questions': post.questions})

        return {
            "status": True
        }

    except Exception as e:
        return {
            "status": False,
            "error": e
        }


@app.delete("/deletePost")
def deletePost(post_id: str):
    try:
        db.collection(u"posts").document(post_id).delete()

        return {
            'status': True
        }

    except Exception as e:
        print(e)
        return {
            'status': False,
            'error': e
        }


@app.post("/addCourse")
def addCourse(course: models.course):
    try:
        doc_ref = db.collection(u"courses")
        data = {
            "description": course.description,
            "enrollments": 0,
            "name": course.name,
            "rating": 0,
            "posts": course.posts,
            "recommended_courses": course.recommended_courses
        }

        doc_ref.add(data)

        return {
            "status": True
        }

    except Exception as e:
        print(e)
        return {
            "status": False,
            "error": e
        }


@app.delete("/deleteCourse")
def deleteCourse(course_id: str):
    try:
        db.collection(u"courses").document(course_id).delete()

        return {
            'status': True
        }

    except Exception as e:
        print(e)
        return {
            'status': False,
            'error': e
        }
        return {"status": False, "error": e}

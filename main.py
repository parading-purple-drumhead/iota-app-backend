import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from fastapi import FastAPI
from pydantic import BaseModel
import datetime

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI()


class post(BaseModel):
    title: str
    post_type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: str = None
    url: str = None
    resource_url: str = None
    content: str = None
    questions: list = None


class user(BaseModel):
    name: str
    avatar: str
    email: str
    phone: int
    points: int


@app.post("/addPost")
def addPost(post: post):

    try:
        doc_ref = db.collection(u"posts")
        data = {
            u"title": post.title,
            u"type": post.type,
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


@app.delete("/deleteCourse")
def deleteCourse(course_id: str):
    try:
        db.collection(u"courses").document(course_id).delete()
        return{
            'status': True
        }
    except Exception as e:
        print(e)
        return {
            'status': False,
            'error': e
        }

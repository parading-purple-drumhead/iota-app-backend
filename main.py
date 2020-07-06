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

class course(BaseModel):
    description: str
    enrollments: int
    name: str
    rating: float
    posts: list = None
    recommended_courses: list = None

@app.post("/addPost")
def addPost(post: post):

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
        return {"status": True}

    except Exception as e:
        print(e)
        return {"status": False, "error": e}

@app.post("/addCourse")
def addCourse(course: course):
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
        return {"status": True}
    except Exception as e:
        print(e)
        return {"status": False, "error": e}
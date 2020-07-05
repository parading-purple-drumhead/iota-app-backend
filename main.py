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


@app.post("/addPost")
def addPost(post: post):
    try:
        doc_ref = db.collection(u"posts")
        if post.post_type == "video":
            doc_ref.add(
                {
                    u"title": post.title,
                    u"type": post.post_type,
                    u"created_at": datetime.datetime.now(),
                    u"updated_at": datetime.datetime.now(),
                    u"description": post.description,
                    u"url": post.url,
                    u"resource_url": post.resource_url,
                }
            )
        elif post.post_type == "article":
            doc_ref.add(
                {
                    u"title": post.title,
                    u"type": post.post_type,
                    u"created_at": datetime.datetime.now(),
                    u"updated_at": datetime.datetime.now(),
                    u"content": post.content,
                    u"resource_url": post.resource_url,
                }
            )
        elif post.post_type == "quiz":
            doc_ref.add(
                {
                    u"title": post.title,
                    u"type": post.post_type,
                    u"created_at": datetime.datetime.now(),
                    u"updated_at": datetime.datetime.now(),
                    u"questions": post.questions,
                }
            )
        return {"status": True}
    except Exception as e:
        print(e)
        return {"status": False, "error": e}


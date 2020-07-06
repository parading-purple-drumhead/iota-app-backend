from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import firestore, credentials
import datetime

cred = credentials.Certificate("C:/Users/hp/Desktop/Dishyanth/project/iota app try/fastapi try/iotaapp-5076c-firebase-adminsdk-zbw8b-382bb019a3.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI(debug = True)


class post(BaseModel):

    document:str 
    post_type:str
    title:str = None
    url:str = None
    resource_url:str = None
    description:str = None
    content:str = None
    questions:list = None



@app.post("/post")
async def post(post:post):

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
        return{"message":"True"}

    except Exception as e:
        return {"message":"False","Exception":e}
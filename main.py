from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pyrebase
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate("./iotaapp-5076c-firebase-adminsdk-zbw8b-8f637efbc2.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

class user(BaseModel):
    name: str
    avatar: str
    email: str
    phone: int
    points: int

app = FastAPI()

@app.delete("/delete_post")
def deletePost(post_id:str):
    try:
        db.collection(u"posts").document(post_id).delete()
        return{
            'status':True
        }
    except Exception as e:
        print(e)
        return{
            'status':False,
            'error':e
        }

@app.delete("/delete_course")
def deleteCourse(course_id:str):
    try:
        db.collection(u"courses").document(course_id).delete()
        return{
            'status':True
        }
    except Exception as e:
        print(e)
        return{
            'status':False,
            'error':e
        }
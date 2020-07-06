from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import firestore, credentials
import datetime

cred = credentials.Certificate("C:/Users/hp/Desktop/Dishyanth/project/iota app try/fastapi try/iotaapp-5076c-firebase-adminsdk-zbw8b-382bb019a3.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = FastAPI(debug = True)

class course(BaseModel):

    document:str 
    name:str = None
    post:list = None
    recommended_courses:list = None
    rating:float = None
    description:str = None
    enrollment:int = None
    

@app.post("/course")
async def course(course:course):

    try:
        edit = db.collection(u'courses').document(course.document)
        edit.update({u'name': course.name})
        edit.update({u'post': course.post})
        edit.update({u'recommended_courses': course.recommended_courses})
        edit.update({u'rating': course.rating})
        edit.update({u'description': course.description})
        edit.update({u'enrollment': course.enrollment})

        return{"message":"True"}

    except Exception as e:
        return {"message":"False","error":e}
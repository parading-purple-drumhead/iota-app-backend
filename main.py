from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import firestore, credentials
import datetime

cred = credentials.Certificate("C:/Users/hp/Desktop/Dishyanth/project/iota app try/fastapi try/iotaapp-5076c-firebase-adminsdk-zbw8b-382bb019a3.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI(debug = True)


class editpost(BaseModel):

	document:str 
	post_type:str
	title:str = None
	url:str = None
	resource_url:str = None
	description:str = None
	content:str = None
	questions:list = None



@app.post("/editpost")
async def editpost(editpost:editpost):

	try:

		edit = db.collection(u'posts').document(editpost.document)
		edit.update({u'title': editpost.title})
		edit.update({u'updated_at': firestore.SERVER_TIMESTAMP})

		if editpost.post_type == "video":

			edit.update({u'description': editpost.description})
			edit.update({u'resource_url': editpost.resource_url})
			edit.update({u'url': editpost.url})

		elif editpost.post_type == "article":

			edit.update({u'content': editpost.content})
			edit.update({u'resource_url': editpost.resource_url})

		else:
			edit.update({u'questions': editpost.questions})
		return{"message":"True"}

	except Exception as e:
		return {"message":"False","Exception":e}
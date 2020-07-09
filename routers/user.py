from fastapi import APIRouter, HTTPException
from models import User
from routers import db, tokenverify

router = APIRouter()

@router.get("/{user_id}")
def get_userInfo(user_id):

    try:
        user = db.collection(u"users").document(user_id).get().to_dict()
        return user

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/add")
def add_post(user: User):
    try:
        print("new test here")
        doc_ref =  db.collection(u"users")
        doc_ref.add(dict(user))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
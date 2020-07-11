from fastapi import APIRouter, HTTPException
from models import User
from routers import db
from google.api_core.exceptions import AlreadyExists

router = APIRouter()


@router.get("/{user_id}", response_model=User)
def get_user_info(user_id):

    try:
        user = db.collection(u"users").document(user_id).get().to_dict()
        return user

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}")
def edit_user(user_id, user: User):
    try:
        edit = db.collection(u"users").document(user_id)
        edit.update(user.dict(exclude_none=True, exclude_defaults=True))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{user_id}/add")
def add_user(user_id, user: User):
    try:
        doc_ref = db.collection(u"users")
        doc_ref.add(dict(user), document_id=user_id)

    except AlreadyExists as e:
        print(e)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
def delete_user(user_id):
    try:
        db.collection(u"users").document(user_id).delete()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

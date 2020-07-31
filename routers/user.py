from fastapi import APIRouter, HTTPException, Request
from models import User, Progress
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


@router.post("/{course_id}/{post_id}/progress")
def progress(request: Request, course_id, post_id, progress: Progress):
    try:
        user_id = request.headers.get("uid")
        ed = db.collection(u"users").document(user_id).collection(u"progress")
        edi = ed.document(course_id).collection("post_progress")
        edit = edi.document(post_id)
        post_progress = edi.collection("post_progress").stream()
        post_count = 0
        post_completed = 0

        edit.update({u"progress": progress.progress})

        for post in post_progress:
            post_count = post_count + 1
            sums1 = edi.collection("post_progress").document(post.id)
            sums = sums1.get().to_dict()
            if sums["progress"] == "1":
                post_completed = post_completed + 1

        course_progress = post_completed/post_count
        edi.update({u"course_progress": course_progress})

        return{
            "courseProgress": course_progress,
            "postProgress": progress.progress
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

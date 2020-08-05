from fastapi import APIRouter, HTTPException, Request
from models import User, Progress
from routers import db
from google.api_core.exceptions import AlreadyExists
from firebase_admin import firestore

router = APIRouter()


def recomended_course(user_id):
    try:
        courses = db.collection(u"users").document(user_id).collection(u"progress").stream()
        course = []
        for reco in courses:
            course.append(reco.id)

        i = 0
        j = 0
        recomended_course = set()
        for i in range(len(course)):
            q = db.collection("courses").document(course[i]).get().to_dict()
            for j in range(len(q["recommended_courses"])):
                recomended_course.add(q["recommended_courses"][j])
                j = j + 1

            i = i + 1

        recommended_courses = list(recomended_course)
        k = 0
        for k in range(len(recommended_courses)):
            edit = db.collection(u"users").document(user_id)
            edit.update({
                u"recomended_course": firestore.ArrayUnion([recommended_courses[k]])
                })
            k = k + 1

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=User)
def get_user_info(user_id):

    try:
        recomended_course(user_id)
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
        edi = db.collection(u"users").document(user_id).collection(u"progress").document(course_id)
        edit = edi.collection("post_progress").document(post_id)
        post_progress = edi.collection("post_progress").stream()
        post_count = 0
        post_completed = 0

        edit.update({u"progress": progress.progress})

        for post in post_progress:
            post_count = post_count + 1
            sums = edi.collection("post_progress").document(post.id).get().to_dict()
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

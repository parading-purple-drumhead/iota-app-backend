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
        print(recommended_courses)
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
        user_ref = db.collection(u"users").document(user_id)
        user = user_ref.get().to_dict()
        progress = user_ref.collection("progress").get()
        user["progress"] = []
        for doc in progress:
            doc_dict = doc.to_dict()
            doc_dict["id"] = doc.id
            user["progress"].append(doc_dict)
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


@router.post("/{course_id}/progress")
def progress(request: Request, course_id, progress: Progress):
    try:
        uid = request.headers.get("uid")
        update = db.collection(u"users").document(uid).collection(u"progress").document(course_id)
        update.set({u"post_progress": {progress.post_id: progress.progress}}, merge=True)
        edit = update.get().to_dict()
        post_count = len(edit["post_progress"])
        post_completed = 0
        for i in range(post_count):
            if list(edit["post_progress"].values())[i] == "1":
                post_completed = post_completed + 1

            i = i + 1

        count = db.collection(u"courses").document(course_id).collection("chapters").stream()

        chapters = []
        post_c = 0
        for chap in count:
            chapters.append(chap.id)

        c = db.collection(u"courses").document(course_id).collection("chapters")
        for i in range(len(chapters)):
            counts = c.document(chapters[i]).get().to_dict()
            k = len(counts["post_ids"])
            post_c = post_c + k

        course_progress = post_completed/post_c

        return{
            course_id: {
                "courseProgress": course_progress
            }
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

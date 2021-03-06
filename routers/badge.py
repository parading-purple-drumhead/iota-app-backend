from fastapi import APIRouter, HTTPException, Request
from models import Badge
from routers import db
from typing import Dict

router = APIRouter()


# @router.get("/calculate", response_model=Badge)
def calculate_badge(uid):
    try:
        # uid = request.headers.get("uid")
        user_ref = db.collection(u"users").document(uid)
        user = user_ref.get().to_dict()

        badges = []
        badge_points = []
        badges_ref = db.collection(u"badges").get()
        for badge_ref in badges_ref:
            badge = badge_ref.to_dict()
            badge_points.append(badge["requirement"])
            badges.append(badge)

        index = 0
        for i in range(len(badge_points)):
            if(user["points"] >= badge_points[i] and user["points"] < badge_points[i+1]):
                index = i
                break

        return badges[index]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=e)


@router.get("", response_model=Dict[str, Badge])
def get_all_badge():
    try:
        badge_ref = db.collection(u"badges").stream()
        data = {}
        for badge in badge_ref:
            data[badge.id] = badge.to_dict()
        return data

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{badge_id}", response_model=Badge)
def get_badge(badge_id):
    try:
        badge = db.collection(u"badges").document(badge_id).get().to_dict()
        return badge

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add")
def add_badge(badge: Badge, request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid).get().to_dict()
        if user["admin"]:
            badge_ref = db.collection(u"badges")
            badge_ref.add(dict(badge))
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{badge_id}")
def edit_badge(badge_id, badge: Badge, request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid).get().to_dict()
        if user["admin"]:
            badge_ref = db.collection(u"badges").document(badge_id)
            badge_ref.update(badge.dict(exclude_none=True, exclude_defaults=True))
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{badge_id}")
def delete_badge(badge_id, request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid).get().to_dict()
        if user["admin"]:
            badge_ref = db.collection(u"badges").document(badge_id)
            badge_ref.delete()
        else:
            raise Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

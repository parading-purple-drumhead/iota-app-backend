from fastapi import APIRouter, HTTPException
from models import Badge
from routers import db
from typing import Dict

router = APIRouter()


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
def add_badge(badge: Badge):
    try:
        badge_ref = db.collection(u"badges")
        badge_ref.add(dict(badge))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{badge_id}")
def edit_badge(badge_id, badge: Badge):
    try:

        doc_ref = db.collection(u"badges").document(badge_id)
        doc_ref.update(badge.dict(exclude_none=True, exclude_defaults=True))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{badge_id}")
def delete_badge(badge_id):
    try:

        doc_ref = db.collection(u"badges").document(badge_id)
        doc_ref.delete()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

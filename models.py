from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List, Dict,Literal
from pydantic import AnyUrl, EmailStr
from pytz import timezone


class Post(BaseModel):
    title: Optional[str]
    type: Optional[Literal["article", "quiz", "video"]]
    created_at: datetime = datetime.now(timezone("Asia/Kolkata"))
    updated_at: datetime = datetime.now(timezone("Asia/Kolkata"))
    description: Optional[str]
    url: Optional[str]
    resource_url: Optional[AnyUrl]
    content: Optional[str]
    questions: Optional[List[str]] = []


class Badge(BaseModel):
    image: Optional[str]
    name: Optional[str]
    requirement: Optional[str]


class Course(BaseModel):
    description: Optional[str]
    enrollments: Optional[int] = 0
    name: Optional[str]
    rating: Optional[float] = 0.0
    posts: Optional[List[str]] = []
    recommended_courses: Optional[List[str]] = []


class User(BaseModel):
    name: Optional[str]
    avatar: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[int]
    points: Optional[int] = 0
    college: Optional[str]
    joined: datetime = datetime.now(timezone("Asia/Kolkata"))
    badge: Optional[List[str]] = []
    bookmarks: Optional[List[str]] = []
    activity: Optional[Dict[str, int]]= None

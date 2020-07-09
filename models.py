from pydantic import BaseModel
from typing import Optional, Literal, List
from pydantic import AnyUrl, EmailStr
import datetime


class Post(BaseModel):
    title: Optional[str]
    type: Optional[Literal["article", "quiz", "video"]]
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    description: Optional[str]
    url: Optional[str]
    resource_url: Optional[AnyUrl]
    content: Optional[str]
    questions: Optional[List[str]] = []


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

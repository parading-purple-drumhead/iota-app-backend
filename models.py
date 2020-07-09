from pydantic import BaseModel
from typing import Optional, Literal, List
import datetime


class Post(BaseModel):
    title: str
    type: Literal['article', 'quiz', 'video']
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    description: Optional[str]
    url: Optional[str]
    resource_url: Optional[str]
    content: Optional[str]
    questions: Optional[str]


class Course(BaseModel):
    description: Optional[str]
    enrollments: Optional[int]
    name: Optional[str]
    rating: Optional[float]
    posts: List[str] = []
    recommended_courses: List[str] = []


class user(BaseModel):
    name: str
    avatar: str
    email: str
    phone: int
    points: int
    token_sent: str
    uid_sent: str

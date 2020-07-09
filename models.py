from pydantic import BaseModel
from typing_extensions import Literal
from typing import Optional
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


class course(BaseModel):
    description: str = None
    enrollments: int = None
    name: str = None
    rating: float = None
    posts: list = None
    recommended_courses: list = None
    token_sent: str
    uid_sent: str
    course_id: str = None


class User(BaseModel):
    name: str
    avatar: Optional[str]
    email: str
    phone: Optional[int]
    points: int = 0

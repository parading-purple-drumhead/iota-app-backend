from pydantic import BaseModel
import datetime


class post(BaseModel):
    title: str
    post_type: str
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    description: str = None
    url: str = None
    resource_url: str = None
    content: str = None
    questions: list = None
    token_sent: str
    uid_sent: str
    post_id: str = None


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


class user(BaseModel):
    name: str
    avatar: str
    email: str
    phone: int
    points: int
    token_sent: str
    uid_sent: str
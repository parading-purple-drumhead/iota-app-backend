from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Literal
from pydantic import AnyUrl, EmailStr
from pytz import timezone


class Comment(BaseModel):
    user_id: str
    content: str


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
    comments: Optional[Comment]


class Badge(BaseModel):
    image: Optional[str]
    name: Optional[str]
    requirement: Optional[str]


class Course(BaseModel):
    description: Optional[str]
    enrollments: Optional[List[str]] = []
    name: Optional[str]
    rating: Optional[float] = 0.0
    chapters: Optional[List[str]] = []
    recommended_courses: Optional[List[str]] = []


class Chapter(BaseModel):
    title: Optional[str]
    posts: Optional[List[str]] = []


class User(BaseModel):
    name: Optional[str]
    avatar: Optional[str]
    admin: Optional[bool]
    email: Optional[EmailStr]
    phone: Optional[int]
    points: Optional[int] = 0
    college: Optional[str]
    joined: datetime = datetime.now(timezone("Asia/Kolkata"))
    badge: Optional[List[str]] = []
    bookmarks: Optional[List[str]] = []
    activity: Optional[Dict[str, int]] = None


class Question(BaseModel):
    question: Optional[str]
    option: Optional[Dict[str, str]]
    answer: Optional[List[str]]
    difficulty: Optional[str]
    number: Optional[int]


class Quiz(BaseModel):
    question_id: Optional[str]
    answer: Optional[str]


class QuestionA(BaseModel):
    question: Optional[str]
    option: Optional[Dict[str, str]]
    difficulty: Optional[str]

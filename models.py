from pydantic import BaseModel
<<<<<<< HEAD
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
    user_id: str
    specific: str
=======
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
    posts: Optional[List[str]] = []
    recommended_courses: Optional[List[str]] = []


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
>>>>>>> 223ff556468e709c357ecdcef2955149aaf5ddba

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr

# Schema for the API using pydantic model


class Idea(BaseModel):
    shortname: str
    define: str
    objective: str
    businessvalue: Optional[str] = None
    contact: Optional[str] = None
    status: str
    createdby: str
    datasources: Optional[str]


class UpdateStatus(BaseModel):
    status: str


class Response(BaseModel):
    shortname: str
    define: str
    contact: str
    status: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: str
    id: int
    # password: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Comments(BaseModel):

    id: int
    comments: Optional[str] = None
    createdby: str


class CommentsRes(BaseModel):
    id: int
    comments: str
    createdby: str

    class Config:
        from_attributes = True

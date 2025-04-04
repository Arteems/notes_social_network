from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator


class CreateUser(BaseModel):
    username: str
    mail: EmailStr
    password: str


class User(BaseModel):
    id: str
    username: str
    mail: EmailStr


class UpdateUser(BaseModel):
    username: str | None = None
    password: str | None = None
    mail: EmailStr | None = None

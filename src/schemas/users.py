from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    username: str
    mail: EmailStr
    password: str


class User(CreateUser):
    id: str


class DeleteUser(BaseModel):
    id: str


class UpdateUser(BaseModel):
    username: str | None = None
    password: str | None = None
    mail: EmailStr | None = None

from pydantic import EmailStr, BaseModel


class CreateUser(BaseModel):
    username: str
    mail: EmailStr
    password: str
    role: str


class User(CreateUser):
    user_id: str


class DeleteUser(BaseModel):
    user_id: str


class UpdateUser(BaseModel):
    username: str | None
    password: str | None
    mail: EmailStr | None
    role: str

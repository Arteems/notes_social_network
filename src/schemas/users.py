from pydantic import EmailStr, BaseModel


class User(BaseModel):
    user_id: str
    username: str
    mail: EmailStr
    password: str


class UserCreate(BaseModel):
    username: str
    mail: EmailStr
    password: str


class DeleteUser(BaseModel):
    user_id: str


class UpdateUser(BaseModel):
    username: str | None
    password: str | None
    mail: EmailStr | None





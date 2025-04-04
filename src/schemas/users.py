from pydantic import EmailStr, BaseModel


class CreateUser(BaseModel):
    username: str
    mail: EmailStr
    password: str
    role: str


class User(CreateUser):
    id: str


# class DeleteUser(BaseModel):
#     user_id: str


class UpdateUser(BaseModel):
    username: str | None = None
    password: str | None = None
    mail: EmailStr | None = None
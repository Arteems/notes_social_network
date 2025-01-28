from pydantic import EmailStr

from src.repositories.repository import Repository
from src.schemas.users import User, CreateUser, UpdateUser
from src.exceptions.user_exceptions import UserNotFoundError, UserUpdateError


class UserService:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def get(self, user_id: str) -> User:
        user = await self.repository.get(user_id)
        if not user:
            raise UserNotFoundError(user_id=user_id)
        return User(**user)

    async def create(self, user: CreateUser) -> str:
        result = await self.repository.create(user.model_dump())
        return result

    async def update(self, user_id: str, new_data: UpdateUser) -> User:
        result = await self.repository.update(user_id, new_data.model_dump(exclude_unset=True))
        if not result:
            raise UserUpdateError(user_id)

        return User(**result)

    async def delete(self, user_id: str) -> bool:
        await self.get(user_id)
        return await self.repository.delete(user_id)

    async def update_mail(self, user_id: str, new_mail: EmailStr) -> User:
        return await self.update(user_id=user_id, new_data=UpdateUser(mail=new_mail))

    async def update_password(self, user_id, new_password: str) -> User:
        return await self.update(user_id=user_id, new_data=UpdateUser(password=new_password))

    async def update_username(self, user_id, new_username: str) -> User:
        return await self.update(user_id=user_id, new_data=UpdateUser(username=new_username))









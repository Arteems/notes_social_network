from pydantic import EmailStr

from exceptions.user_exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from repositories import MongoRepository
from exceptions.user_exceptions import (
    InvalidUserRoleError,
    UserNotFoundError,
    UserUpdateError,
)
from schemas.note import CreateNote, Note, UpdateNote
from schemas.users import CreateUser, UpdateUser, User
from services.notes import NoteService


class UserService:
    """Сервис для работы с пользователем"""

    def __init__(self, user_repository: MongoRepository, note_service: NoteService):
        self.__user_repository = user_repository
        self.__note_service = note_service

    async def get(self, user_id: str) -> User:
        user = await self.__user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return User(**user)

    async def get_by_username(self, username: str) -> User:
        user = await self.__user_repository.get_user_by_username(username)
        if not user:
            raise UserNotFoundError(username)
        return User(**user)

    async def get_by_mail(self, email: EmailStr) -> User:
        user = await self.__user_repository.get_user_by_mail(str(email))
        if not user:
            raise UserNotFoundError(email)
        return User(**user)

    async def create(self, new_user: CreateUser) -> str:
        try:
            if await self.get_by_mail(new_user.mail) is not None:
                raise EmailAlreadyExistsError(str(new_user.mail))
            if await self.get_by_username(new_user.username) is not None:
                raise UsernameAlreadyExistsError(new_user.username)
        except UserNotFoundError:
            result = await self.__user_repository.create(new_user.model_dump())
            return result

    async def update(self, user_id: str, new_data: UpdateUser) -> User:
        result = await self.__user_repository.update(
            user_id, new_data.model_dump(exclude_unset=True)
        )
        if not result:
            raise UserUpdateError(user_id)
        return User(**result)

    async def delete(self, user_id: str) -> bool:
        await self.get(user_id)
        return await self.__user_repository.delete(user_id)

    async def update_mail(self, user_id: str, new_mail: EmailStr) -> User:
        return await self.update(user_id=user_id, new_data=UpdateUser(mail=new_mail))

    async def update_password(self, user_id, new_password: str) -> User:
        return await self.update(
            user_id=user_id, new_data=UpdateUser(password=new_password)
        )

    async def update_username(self, user_id, new_username: str) -> User:
        return await self.update(
            user_id=user_id, new_data=UpdateUser(username=new_username)
        )

    async def get_note(self, user_id: str, note_id: str) -> Note:
        user = await self.get(user_id)
        note = await self.__note_service.get(note_id)
        if (
            (user.id != note.owner_id)
            or (user.id not in note.editors)
            or (user.id not in note.viewers)
        ):
            raise InvalidUserRoleError(user_id)
        return note

    async def add_note(self, user_id: str, data: CreateNote) -> str:
        await self.get(user_id)
        result = await self.__note_service.create(data.model_dump())
        return result

    async def delete_note(self, user_id: str, note_id: str) -> bool:
        note = await self.get_note(user_id, note_id)
        if user_id != note.owner_id:
            raise InvalidUserRoleError(user_id)
        return await self.__note_service.delete(note_id)

    async def update_note(
        self, user_id: str, note_id: str, update_data: UpdateNote
    ) -> Note:
        note = await self.get_note(user_id, note_id)
        if (user_id != note.owner_id) or (user_id not in note.editors):
            raise InvalidUserRoleError(user_id)
        return await self.__note_service.update(note_id, update_data)

    async def add_viewer(self, user_id: str, viewer_id: str, note_id: str) -> bool:
        note = await self.get_note(user_id, note_id)
        if user_id != note.owner_id:
            raise InvalidUserRoleError(user_id)
        return await self.__note_service.add_viewer(viewer_id, note_id)

    async def add_editor(self, user_id: str, editor_id: str, note_id) -> bool:
        note = await self.get_note(user_id, note_id)
        if user_id != note.owner_id:
            raise InvalidUserRoleError(user_id)
        return await self.__note_service.add_editor(editor_id, note_id)

    async def delete_viewer(self, user_id: str, viewer_id: str, note_id: str) -> bool:
        note = await self.get_note(user_id, note_id)
        if user_id != note.owner_id:
            raise InvalidUserRoleError(user_id)
        return await self.__note_service.delete_viewer(viewer_id, note_id)

    async def delete_editor(self, user_id: str, editor_id: str, note_id: str) -> bool:
        note = await self.get_note(user_id, note_id)
        if user_id != note.owner_id:
            raise InvalidUserRoleError(user_id)
        return await self.__note_service.delete_editor(editor_id, note_id)

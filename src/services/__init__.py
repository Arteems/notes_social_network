from repositories import notes_repository, users_repository

from .notes import NoteService
from .users import UserService

user_service = UserService(users_repository, NoteService(notes_repository))

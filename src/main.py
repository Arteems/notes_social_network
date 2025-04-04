from fastapi import FastAPI

from api.routers.access_router import access_router
from api.routers.notes_router import notes_router
from api.routers.users_router import users_router

app = FastAPI()
app.include_router(users_router)
app.include_router(notes_router)
# app.include_router(access_router)

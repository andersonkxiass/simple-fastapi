from fastapi import FastAPI

from .database.database import engine, Base
from .routers import files, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(files.router)

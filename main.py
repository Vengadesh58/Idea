from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import ideas, users, auth, comments
from .config import settings

# import models
models.Base.metadata.create_all(bind=engine)

# APP initialization
app = FastAPI()
app.include_router(ideas.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(comments.router)
# app.include_router(likes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

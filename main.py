from fastapi import FastAPI, Response, status, HTTPException, Depends
# import psycopg2
# from psycopg2.extras import RealDictCursor
from typing import List
import time
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .routers import ideas, users, auth, comments


# import models
models.Base.metadata.create_all(bind=engine)

# APP initialization
app = FastAPI()
app.include_router(ideas.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(comments.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

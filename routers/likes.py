from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, File, UploadFile
from typing import Annotated


router = APIRouter(
    prefix="/likes", tags=['likes']
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_likes(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM ideas """)
    # ideas = cursor.fetchall()
    # print(ideas)
    likes = db.query(models.Likes).all()
    return likes


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_likes(db: Session = Depends(get_db), like=schemas.Likes, current_user: int = 5):

    if (like.dir == 1):

        db.query(models.Likes).filter(models.Likes.ideas_id ==
                                      like.idea_id, models.Likes.user_id == current_user)
    else:
        return {}

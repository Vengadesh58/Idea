from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, File, UploadFile
from typing import Annotated

router = APIRouter(
    prefix="/comments", tags=['comments']
)


@router.get("/")
async def get_comments(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM ideas """)
    # ideas = cursor.fetchall()
    # print(ideas)
    ideas = db.query(models.Comments).all()
    return ideas


@router.get("/{id}")
async def get_single_comment(id: int, response: Response, db: Session = Depends(get_db)):
    comment = db.query(models.Comments).filter(models.Comments.id == id).all()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"idea id {id} is not available")

    return comment


@router.put("/{id}")
async def update_comments(id: int, response: Response, comments: schemas.Comments, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE ideas SET shortname = %s, define = %s,objective = %s,businessvalue = %s,contact = %s,status = %s,createdby = %s  WHERE id = %s RETURNING *""",
    # (idea.shortName, idea.define, idea.objective, idea.businessValue, idea.contacts, idea.status, idea.createdby, id))
    # updated = cursor.fetchone()
    # conn.commit()
    update = db.query(models.Comments).filter(models.Comments.id == id)
    post = update.first()

    if post != None:
        update.update(comments.model_dump(), synchronize_session=False)
        db.commit()
        return [update.first()]
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Idea ID {id} is not available in the DB")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentsRes)
async def create_comments(Comments: schemas.Comments, db: Session = Depends(get_db)):
    # cursor.execute(
    # """ INSERT INTO ideas (shortname,define,objective,businessvalue,contact,status,createdby) VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING * """, (Idea.shortName, Idea.define, Idea.objective, Idea.businessValue, Idea.contacts, Idea.status, Idea.createdby))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Comments(**Comments.model_dump())
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

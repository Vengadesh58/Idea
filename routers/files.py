from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, File, UploadFile
from typing import Annotated
from base64 import b64decode
router = APIRouter(
    prefix="/files", tags=['files']
)


@router.put("/{id}")
async def update_files(id: int, response: Response, file: schemas.Files, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE ideas SET shortname = %s, define = %s,objective = %s,businessvalue = %s,contact = %s,status = %s,createdby = %s  WHERE id = %s RETURNING *""",
    # (idea.shortName, idea.define, idea.objective, idea.businessValue, idea.contacts, idea.status, idea.createdby, id))
    # updated = cursor.fetchone()
    # conn.commit()
    update = db.query(models.Files).filter(models.Files.id == id)
    post = update.first()

    if post != None:
        update.update(file.model_dump(), synchronize_session=False)
        db.commit()
        return [update.first()]
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Idea ID {id} is not available in the DB")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Files)
async def create_files(Comments: schemas.Files, db: Session = Depends(get_db)):
    # cursor.execute(
    # """ INSERT INTO ideas (shortname,define,objective,businessvalue,contact,status,createdby) VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING * """, (Idea.shortName, Idea.define, Idea.objective, Idea.businessValue, Idea.contacts, Idea.status, Idea.createdby))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Files(**Comments.model_dump())
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}")
async def get_files(id: int, response: Response, db: Session = Depends(get_db)):
    comment = db.query(models.Files).filter(models.Files.id == id).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"idea id {id} is not available")

    base_64 = comment
    byte = b64decode(base_64, validate=True)

    if byte[0:4] != b'%PDF':
        raise ValueError("Missing the pdf file signature")

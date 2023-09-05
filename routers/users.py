from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users", tags=['users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hased_password = utils.hash(user.password)
    user.password = hased_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{email}", response_model=schemas.UserOut)
async def get_users(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {email} not exist")
    return user


@router.delete("/{email}", response_model=schemas.UserOut)
async def delete_users(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email)

    if user.first() != None:
        user.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                            detail=f"Idea ID {email} is deleted from the list")
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"Idea ID {email} is not available in the DB")

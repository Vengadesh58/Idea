from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, File, UploadFile
from base64 import b64decode
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/files", tags=['files']
)


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_location = f"/data/fastapi/{file.filename}"

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    return {"message": f"Successfully uploaded {file.filename}"}


@router.get("/downloadfile/")
def download_file():
    # Replace with the actual path to your file
    file_path = "/data/fastapi/sample.pdf"
    return FileResponse(file_path, headers={"Content-Disposition": "attachment"})

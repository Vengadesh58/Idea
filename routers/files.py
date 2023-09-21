from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, File, UploadFile
from base64 import b64decode
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix="/files", tags=['files']
)


@router.post("/uploadfile/{id}", status_code=status.HTTP_201_CREATED)
async def create_upload_file(id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):
    try:
        file_location = f"/data/fastapi/files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        file_dict = {"id": id,
                     "filename": file.filename}
        new_file = models.Files(**file_dict)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        return {"message": f"Successfully uploaded {file.filename}"}

    except:
        file_location = f"C:\\Users\\I355833\\Downloads\\test\\{file.filename}"

        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        file_dict = {"id": id,
                     "filename": file.filename}
        new_file = models.Files(**file_dict)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

    return {"message": f"Successfully uploaded {file.filename}"}


@router.get("/downloadfile/{id}")
def download_file(id: int, response: Response, db: Session = Depends(get_db)):

    file_download = db.query(models.Files).filter(
        models.Files.id == id).first()

    print(file_download)
    if not file_download:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"idea id {id} is not available")
    # Replace with the actual path to your file
    try:
        file_path = f"/data/fastapi/files/{file_download.filename}"
        # Use the actual content type if available, otherwise, use 'application/octet-stream'
        # content_type = file_download.content_type or 'application/octet-stream'

        response.headers["Content-Disposition"] = f'attachment; filename="{file_download.filename}"'
        # response.headers["Content-Type"] = content_type
        response.headers["Content-Length"] = str(os.path.getsize(file_path))
        return FileResponse(file_path)

    except:
        file_path = f"C:\\Users\\I355833\\Downloads\\test\\{file_download.filename}"
        # Use the actual content type if available, otherwise, use 'application/octet-stream'
        # content_type = file_download.content_type or 'application/octet-stream'

        response.headers["Content-Disposition"] = f'attachment; filename="{file_download.filename}"'
        # response.headers["Content-Type"] = content_type
        response.headers["Content-Length"] = str(os.path.getsize(file_path))
        return FileResponse(file_path)

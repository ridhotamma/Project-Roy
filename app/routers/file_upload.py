from fastapi import APIRouter, UploadFile, File, status
from fastapi.exceptions import HTTPException
from app.crud.image_upload import upload_to_s3

router = APIRouter()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    try:
        file_url = upload_to_s3(file_location, file.filename)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"[Upload Endpoint] Unexpected Error: {e}",
            },
        )

    return {"file_url": file_url}

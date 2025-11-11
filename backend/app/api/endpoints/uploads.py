import shutil
from pathlib import Path
from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse

router = APIRouter()

@router.post("/", response_model=dict)
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads an image, saves it to the static directory, and returns the URL.
    """
    try:
        # Define the path to save the uploaded file
        upload_dir = Path("app/static/images")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.filename
        
        # Save the file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return the URL of the uploaded file
        file_url = f"/static/images/{file.filename}"
        return JSONResponse(status_code=200, content={"file_url": file_url})
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"There was an error uploading the file: {e}"})


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import shutil

app = FastAPI()
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


app.mount(
    "/files",
    StaticFiles(directory=UPLOAD_DIR),
    name="files"
)

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="File not selected"
        )
    filename = os.path.basename(filename)
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )

    file_path = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(file_path):
        raise HTTPException(
            status_code=409,
            detail="File already exists"
        )

    try:

        with open(file_path, "xb") as buffer:
            # copyfileobj() copies data from source to destination.
            shutil.copyfileobj(file.file, buffer)

    except OSError:
        raise HTTPException(
            status_code=500,
            detail="File could not be uploaded"
        )

    finally:
        file.file.close()

    return {
        "message": "File uploaded successfully",
        "fileName": filename,

        "file_url": f"/files/{filename}"
    }

@app.get("/files/{filename}")
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


@app.get("/")
def home():

    return {
        "message": "File Upload API Running"
    }


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()


# --------------------------------------------------
# STEP 1: CREATE UPLOADS FOLDER
# --------------------------------------------------

# Folder name where uploaded files will be stored.
UPLOAD_DIR = "uploads"

# Create uploads folder if it does not exist.
# exist_ok=True means:
# If folder already exists, Python will not throw an error.
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --------------------------------------------------
# STEP 2: STATIC FILE CONFIGURATION
# --------------------------------------------------

# Mount the uploads directory with the URL "/files".
#
# StaticFiles automatically serves files from this folder.
#
# Example:
# If test.pdf is stored inside uploads folder,
# it can be accessed using:
# http://127.0.0.1:8000/files/test.pdf
#
# name="files" is the internal name of this mount.
app.mount(
    "/files",
    StaticFiles(directory=UPLOAD_DIR),
    name="files"
)


# --------------------------------------------------
# STEP 3: FILE UPLOAD API
# --------------------------------------------------

# POST API to upload a file.
#
# UploadFile:
# Used to receive uploaded files in FastAPI.
#
# File(...):
# Tells FastAPI that file input is required.
#
# ... means this field is mandatory.
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):

    # Get the original filename from uploaded file.
    filename = file.filename

    # Check whether the user selected a file.
    # If filename is empty, return HTTP 400 error.
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="File not selected"
        )

    # basename() extracts only the filename.
    # It removes any directory path supplied with the filename.
    #
    # Example:
    # C:/Users/test.pdf becomes test.pdf
    filename = os.path.basename(filename)

    # Check filename again after sanitization.
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )

    # Create complete file path.
    #
    # Example:
    # uploads/test.pdf
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Check whether the file already exists.
    # If it exists, return HTTP 409 Conflict.
    # This prevents overwriting an existing file.
    if os.path.exists(file_path):
        raise HTTPException(
            status_code=409,
            detail="File already exists"
        )

    try:

        # Open destination file in binary write mode.
        #
        # "xb" means:
        # x = Create a new file; fail if it already exists.
        # b = Binary mode (required for images, PDFs, etc.).
        with open(file_path, "xb") as buffer:

            # Copy uploaded file content into destination file.
            #
            # file.file = Source uploaded file.
            # buffer = Destination file.
            #
            # copyfileobj() copies data from source to destination.
            shutil.copyfileobj(file.file, buffer)

    except OSError:

        # If file creation or writing fails,
        # return HTTP 500 Internal Server Error.
        raise HTTPException(
            status_code=500,
            detail="File could not be uploaded"
        )

    finally:

        # Close uploaded file after processing.
        # This releases the file resource.
        file.file.close()

    # Return successful upload response.
    return {
        "message": "File uploaded successfully",
        "fileName": filename,

        # Relative URL to access the uploaded file.
        "file_url": f"/files/{filename}"
    }


# --------------------------------------------------
# STEP 4: HOME API
# --------------------------------------------------

# Simple GET API to check whether application is running.
@app.get("/")
def home():

    return {
        "message": "File Upload API Running"
    }

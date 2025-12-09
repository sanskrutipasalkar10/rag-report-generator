import os
from fastapi import UploadFile

UPLOAD_DIR = "uploaded_files"


def ensure_upload_dir():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)


def save_upload_file_tmp(upload_file: UploadFile) -> str:
    """
    Saves uploaded file to /uploaded_files and returns local path.
    """

    ensure_upload_dir()

    file_location = os.path.join(UPLOAD_DIR, upload_file.filename)

    with open(file_location, "wb") as f:
        f.write(upload_file.file.read())

    return file_location

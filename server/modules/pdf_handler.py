import os
import shutil
from fastapi import UploadFile
import tempfile

UPLOAD_DIR = './uploaded_documents'


def save_uploaded_file(files:list[UploadFile])->list[str]: # type: ignore
    os.makedirs(UPLOAD_DIR,exist_ok=True)
    file_paths = []
    for file in files:
        temp_path = os.path.join(UPLOAD_DIR,file.filename) # type: ignore
        with open(temp_path,'wb') as f:
            shutil.copyfileobj(file.file,f)
        file_paths.append(temp_path)
    return file_paths
    
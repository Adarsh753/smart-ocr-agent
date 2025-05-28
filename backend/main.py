from fastapi import FastAPI, UploadFile, File
import shutil
import os
from uuid import uuid4

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Smart OCR Agent is live!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Navigate to the project root directory to reach storage/input
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(BASE_DIR, "storage", "input")
    os.makedirs(input_dir, exist_ok=True)

    task_id = str(uuid4())
    file_path = os.path.join(input_dir, f"{task_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File uploaded successfully", "task_id": task_id}

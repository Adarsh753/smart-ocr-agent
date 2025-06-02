from fastapi import FastAPI, UploadFile, File, status
from fastapi.responses import JSONResponse
import shutil
import os
from uuid import uuid4
from ocr_engine import extract_text
import logging

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Smart OCR Agent is live!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Set up base paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(BASE_DIR, "storage", "input")
    output_dir = os.path.join(BASE_DIR, "storage", "output")

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Validate file type
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.pdf')):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid file type. Please upload an image or PDF file (.png, .jpg, .jpeg, .bmp, .tiff, .pdf)."}
        )

    # Generate task ID and save file
    task_id = str(uuid4())
    file_path = os.path.join(input_dir, f"{task_id}_{file.filename}")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"✅ File saved to: {file_path}")
    except Exception as e:
        print(f"❌ Failed to save file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Failed to save file", "details": str(e)}
        )

    # Run OCR
    try:
        ocr_text = extract_text(file_path)
        print(f"🧠 OCR Text Extracted:\n{ocr_text}")
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "OCR failed", "details": str(e)}
        )

    # Save OCR output
    output_path = os.path.join(output_dir, f"{task_id}.txt")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ocr_text)
        print(f"📄 OCR output saved to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to write OCR output: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Failed to save OCR output", "details": str(e)}
        )

    # Logging
    logging.basicConfig(filename=os.path.join(BASE_DIR, "upload_log.txt"), level=logging.INFO)
    logging.info(f"{task_id} - Uploaded: {file_path} - OCR Output: {output_path}")

    return {
        "message": "File uploaded and OCR complete",
        "task_id": task_id,
        "ocr_output_file": f"{task_id}.txt"
    }

@app.get("/result/{task_id}/")
async def get_ocr_result(task_id: str):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(BASE_DIR, "storage", "output")
    output_file = os.path.join(output_dir, f"{task_id}.txt")

    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                ocr_text = f.read()
            return {"task_id": task_id, "ocr_text": ocr_text}
        except Exception as e:
            print(f"❌ Failed to read OCR output: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Failed to read OCR output", "details": str(e)}
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "OCR result not found for the provided task ID."}
        )

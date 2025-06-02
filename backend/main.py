from fastapi import FastAPI, UploadFile, File, status, APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import shutil
import os
from uuid import uuid4
from ocr_engine import extract_text
import logging

# Load environment variables
load_dotenv()

# Get BASE_DIR and LOG_LEVEL from environment or set defaults
BASE_DIR = os.getenv("BASE_DIR")
if not BASE_DIR:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Setup logging directory and logger
log_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "smart_ocr.log"),
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app and API router for versioning
app = FastAPI(title="Smart OCR Agent")
api_v1 = APIRouter(prefix="/api/v1", tags=["Smart OCR Agent"])

@api_v1.get("/health/", tags=["Health"])
def health_check():
    return {"status": "ok"}

@api_v1.get("/", tags=["Welcome"])
def read_root():
    return {"message": "Smart OCR Agent is live!"}

@api_v1.post("/upload/", tags=["OCR"])
async def upload_file(file: UploadFile = File(...)):
    input_dir = os.path.join(BASE_DIR, "storage", "input")
    output_dir = os.path.join(BASE_DIR, "storage", "output")

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Validate file type
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.pdf')
    if not file.filename.lower().endswith(allowed_extensions):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"}
        )

    task_id = str(uuid4())
    file_path = os.path.join(input_dir, f"{task_id}_{file.filename}")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"{task_id} - File saved to: {file_path}")
    except Exception as e:
        logger.error(f"{task_id} - Failed to save file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Failed to save file", "details": str(e)}
        )

    # Run OCR
    try:
        ocr_text = extract_text(file_path)
        logger.info(f"{task_id} - OCR completed successfully.")
    except Exception as e:
        logger.error(f"{task_id} - OCR failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "OCR failed", "details": str(e)}
        )

    # Save OCR output
    output_path = os.path.join(output_dir, f"{task_id}.txt")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ocr_text)
        logger.info(f"{task_id} - OCR output saved to: {output_path}")
    except Exception as e:
        logger.error(f"{task_id} - Failed to save OCR output: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Failed to save OCR output", "details": str(e)}
        )

    return {
        "message": "File uploaded and OCR complete",
        "task_id": task_id,
        "ocr_output_file": f"{task_id}.txt"
    }

@api_v1.get("/result/{task_id}/", tags=["OCR"])
async def get_ocr_result(task_id: str):
    output_dir = os.path.join(BASE_DIR, "storage", "output")
    output_file = os.path.join(output_dir, f"{task_id}.txt")

    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                ocr_text = f.read()
            return {"task_id": task_id, "ocr_text": ocr_text}
        except Exception as e:
            logger.error(f"{task_id} - Failed to read OCR output: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Failed to read OCR output", "details": str(e)}
            )
    else:
        logger.warning(f"{task_id} - OCR result not found.")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "OCR result not found for the provided task ID."}
        )

# Include API router
app.include_router(api_v1)

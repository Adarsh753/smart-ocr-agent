# 📄 Smart OCR Agent

A FastAPI-based backend service for performing Optical Character Recognition (OCR) on uploaded images and PDF files. It saves the extracted text in a local directory and provides endpoints to retrieve results.

---

## 🚀 Features

✅ Upload images or PDFs for OCR
✅ Extract text from supported files (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.pdf`)
✅ Stores OCR results as text files
✅ REST API with versioning (`/api/v1`)
✅ Environment-based configuration (.env support)
✅ Basic logging to `logs/smart_ocr.log`

---

## 🛠️ Tech Stack

* **FastAPI** — web framework
* **Python** — backend language
* **dotenv** — environment variable management
* **OCR Engine** — import easyocr
		   import cv2

---

## 📁 Project Structure

```
smart_ocr_agent/
├── backend/
│   ├── main.py             # FastAPI application
│   ├── ocr_engine.py       # OCR processing logic
│   └── storage/
│       ├── input/          # Uploaded files
│       └── output/         # Extracted OCR text
├── logs/
│   └── smart_ocr.log       # Logging output
├── .env                    # Environment variables
└── README.md               # Project documentation
```

---

## ⚙️ Setup Instructions

1️⃣ **Clone the repository:**

```bash
git clone https://github.com/yourusername/smart_ocr_agent.git
cd smart_ocr_agent/backend
```

2️⃣ **Create a virtual environment and install dependencies:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ **Create a `.env` file in the `backend` folder (or project root):**

```
BASE_DIR=/absolute/path/to/your/project
LOG_LEVEL=INFO
```

*(Optional: adjust paths as needed.)*

4️⃣ **Run the application:**

```bash
uvicorn main:app --reload
```

5️⃣ **Access the API:**

* Health Check: [http://localhost:8000/api/v1/health/](http://localhost:8000/api/v1/health/)
* Upload OCR File: [http://localhost:8000/api/v1/upload/](http://localhost:8000/api/v1/upload/)
* Get OCR Result: [http://localhost:8000/api/v1/result/{task\_id}/](http://localhost:8000/api/v1/result/{task_id}/)

---

## 🔌 API Endpoints

| Method | Endpoint                    | Description            |
| ------ | --------------------------- | ---------------------- |
| GET    | `/api/v1/health/`           | Health check endpoint  |
| GET    | `/api/v1/`                  | Welcome message        |
| POST   | `/api/v1/upload/`           | Upload a file for OCR  |
| GET    | `/api/v1/result/{task_id}/` | Get extracted OCR text |

---

## 🔍 Notes

* **OCR Engine:** Make sure your `ocr_engine.py` has an `extract_text(file_path)` function that returns extracted text.
* **File Storage:** Files are saved under `storage/input` and `storage/output`.
* **Logging:** Logs are stored in the `logs` folder with details of uploads and processing.

---

## 🤝 Contribution

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or report bugs.

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

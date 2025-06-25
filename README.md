# 🧠 Image to Insight

An AI-powered fullstack application that extracts meaningful insights from images using OCR and NLP.

## 🚀 Features

- 📤 Upload any image (PNG, JPG, etc.)
- 🔍 Extract text using Tesseract OCR
- 🧾 Count number of text lines
- 🏷️ Detect keywords (top meaningful words)
- 📝 Generate quick summary
- ❤️ Analyze sentiment (positive/neutral/negative)
- 🕒 View history of all uploaded images + insights
- 🧼 Noise reduction using OpenCV for better accuracy

---

## 🧠 Tech Stack

| Layer       | Tech Used                             |
|-------------|----------------------------------------|
| Frontend    | React (Hooks, Fetch API)               |
| Backend     | FastAPI (Python), OpenCV, TextBlob     |
| AI/NLP      | Tesseract OCR, TextBlob NLP            |
| Storage     | Local filesystem (image + JSON logs)   |

---

## 🛠️ Getting Started

### 🔧 Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
uvicorn main:app --reload

🌐 Frontend (React)
cd frontend
npm install
npm start

📁 Folder Structure

image-to-insight/
├── backend/
│   ├── main.py
│   ├── ocr_utils.py
│   └── data/               
├── frontend/
│   ├── UploadImage.jsx
│   ├── App.jsx
├── README.md

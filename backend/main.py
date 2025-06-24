from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ocr_utils import process_image
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    result = process_image(contents)
    return {"insights": result}

@app.get("/history/")
def get_all_insights():
    data_dir = "data"
    results = []

    if not os.path.exists(data_dir):
        return JSONResponse(content={"history": []})

    for filename in sorted(os.listdir(data_dir), reverse=True):
        if filename.endswith("_result.json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                insights = json.load(f)
                timestamp = filename.replace("_result.json", "")
                results.append({
                    "timestamp": timestamp,
                    "filename": filename,
                    "insights": insights
                })

    return JSONResponse(content={"history": results})

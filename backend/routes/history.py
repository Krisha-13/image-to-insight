# routes/history.py

import os
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/history/")
def get_all_insights():
    data_dir = "data"
    results = []

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

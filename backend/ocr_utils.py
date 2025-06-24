import pytesseract
from PIL import Image
import io
import re
from collections import Counter
from textblob import TextBlob
import os
import json
from datetime import datetime
import numpy as np
import cv2

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

def extract_keywords(text, top_n=5):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = set([
        "this", "that", "with", "from", "have", "there", "which",
        "your", "will", "been", "were", "them", "then", "they",
        "some", "into", "about", "such", "these", "those"
    ])
    filtered = [w for w in words if w not in stopwords]
    most_common = Counter(filtered).most_common(top_n)
    return [word for word, _ in most_common]

def generate_summary(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return "No content found."
    elif len(lines) == 1:
        return lines[0]
    else:
        return f"{lines[0]} {lines[1]}"

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"

def preprocess_image_for_ocr(pil_image):
    # Convert to OpenCV format
    cv_image = np.array(pil_image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Denoise and threshold
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert back to PIL
    preprocessed_pil = Image.fromarray(thresh)
    return preprocessed_pil

def process_image(image_bytes):
    original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = preprocess_image_for_ocr(original_image)
    extracted_text = pytesseract.image_to_string(image)
    lines = extracted_text.strip().splitlines()

    insights = {
        "text": extracted_text,
        "line_count": len(lines),
        "keywords": extract_keywords(extracted_text),
        "summary": generate_summary(extracted_text),
        "sentiment": get_sentiment(extracted_text),
    }

    # Save image and insights
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = "data"
    os.makedirs(base_path, exist_ok=True)

    # Save original image
    original_image.save(os.path.join(base_path, f"{timestamp}_image.png"))

    # Save insights JSON
    with open(os.path.join(base_path, f"{timestamp}_result.json"), "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=2)

    return insights

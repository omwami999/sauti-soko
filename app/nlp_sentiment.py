from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import os

# Swahili + English model
model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def detect_language(text: str) -> str:
    swahili_words = ['bei', 'sukuma', 'nyanya', 'maziwa', 'mkulima', 'soko']
    if any(word in text.lower() for word in swahili_words):
        return "sw"
    return "en"

def analyze_farmer_review(text: str):
    result = sentiment_pipeline(text[:512])[0]
    return {
        "label": result['label'],
        "score": round(result['score'], 3)
    }
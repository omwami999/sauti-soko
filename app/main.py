from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
import os

from .voice_processor import speech_to_text
from .nlp_sentiment import analyze_farmer_review
from .prices_db import get_current_prices, search_price

app = FastAPI(
    title="SautiSoko API",
    description="Voice-enabled market price checker with farmer sentiment (Swahili & English)",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Karibu SautiSoko! Send voice note → get prices + sentiment"}

@app.post("/voice-price")
async def voice_price_query(audio: UploadFile = File(...)):
    if not audio.filename.endswith(('.wav', '.mp3', '.m4a')):
        raise HTTPException(400, "Support: .wav, .mp3, .m4a")

    contents = await audio.read()
    temp_path = f"/tmp/{audio.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    # Convert voice → text
    text, lang = speech_to_text(temp_path)
    os.remove(temp_path)

    # Detect what commodity they're asking
    commodity = search_price(text.lower())
    if not commodity:
        return {
            "query": text,
            "language": lang,
            "reply": f"Samahani, sikupata bei ya bidhaa uliyouliza. Jaribu tena kwa mfano 'Bei ya sukuma wiki?'"
        }

    # Get current price
    price_info = get_current_prices()[commodity]

    # Optional: analyze sentiment if review-like
    sentiment = analyze_farmer_review(text) if len(text.split()) > 8 else None

    reply = f"Bei ya {commodity} leo ni KSh {price_info['price']}/kg huko {price_info['market']}. "
    if sentiment and sentiment["label"] == "NEGATIVE":
        reply += "Wakulima wanalalamika bei ni ya chini sana."

    return {
        "query": text,
        "language": lang,
        "commodity": commodity,
        "price": price_info,
        "sentiment": sentiment,
        "reply_swahili": reply
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
import speech_recognition as sr
from pydub import AudioSegment
import os

# Support Swahili & English
recognizer = sr.Recognizer()

def speech_to_text(audio_path: str):
    # Convert any format
    audio = AudioSegment.from_file(audio_path)
    wav_path = audio_path + ".wav"
    audio.export(wav_path, format="wav")

    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Try Google 
            text = recognizer.recognize_google(audio_data, language="sw-KE")
            os.remove(wav_path)
            return text, "sw"
        except:
            try:
                text = recognizer.recognize_google(audio_data, language="en-US")
                os.remove(wav_path)
                return text, "en"
            except:
                os.remove(wav_path)
                return "Samahani, sikuweza kusikia vizuri. Tafadhali rudia.", "unknown"
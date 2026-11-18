import sounddevice as sd
from scipy.io import wavfile

import os
from pathlib import Path

from google import genai
from dotenv import load_dotenv


# 1. Load API key
BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found in .env file")


# 2. Connect to Gemini
client = genai.Client(
    api_key=api_key,
    http_options={"api_version": "v1beta"}
)


# 3. Recording settings
duration = 8
sample_rate = 16000

print("Speak your question...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

# 4. Save recording
audio_path = BASE_DIR / "farmer_question.wav"

wavfile.write(
    str(audio_path),
    sample_rate,
    audio
)

print("Recording saved successfully!")


# 5. Upload audio to Gemini
audio_file = client.files.upload(
    file=str(audio_path)
)


transcription = client.interactions.create(
    model="gemini-3.5-transcribe",
    input=[
        {
            "type": "audio",
            "uri": audio_file.uri,
            "mime_type": audio_file.mime_type
        }
    ]
)

print("\nFarmer said:")
print(transcription.output_text)
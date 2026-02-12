import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def transcrever_audio(caminho_audio):

    with open(caminho_audio, "rb") as f:
        audio_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "mime_type": "audio/wav",
                        "data": audio_bytes
                    }
                ]
            }
        ],
    )

    return response.text

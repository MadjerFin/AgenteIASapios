from fastapi import FastAPI
from pydantic import BaseModel
from core.agent import Agent
from services.audio_transcriber import transcrever_audio
import base64
import tempfile
import os

app = FastAPI(
    title="API Triagem Veicular",
    version="1.0.0",
    description="API inteligente para triagem de problemas veiculares"
)

agent = Agent()


# ================================
# MODELOS DE REQUEST
# ================================

class TextoRequest(BaseModel):
    mensagem: str


class AudioRequest(BaseModel):
    audio_base64: str
    formato: str  # ex: wav, mp3


# ================================
# ROTAS BÁSICAS
# ================================

@app.get("/")
def home():
    return {
        "status": "API Triagem Veicular Online",
        "versao": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# ================================
# TRIAGEM VIA TEXTO
# ================================

@app.post("/triagem/texto")
def triagem_texto(request: TextoRequest):

    try:
        resultado = agent.run(request.mensagem)

        return {
            "status": "sucesso",
            "analise": resultado
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e)
        }


# ================================
# TRIAGEM VIA ÁUDIO
# ================================

@app.post("/triagem/audio")
def triagem_audio(request: AudioRequest):

    caminho_temp = None

    try:
        # Decodifica base64
        audio_bytes = base64.b64decode(request.audio_base64)

        # Salva temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{request.formato}") as tmp:
            tmp.write(audio_bytes)
            caminho_temp = tmp.name

        # Transcreve
        texto_transcrito = transcrever_audio(caminho_temp)

        # Analisa
        resultado = agent.run(texto_transcrito)

        return {
            "status": "sucesso",
            "transcricao": texto_transcrito,
            "analise": resultado
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e)
        }

    finally:
        if caminho_temp and os.path.exists(caminho_temp):
            os.remove(caminho_temp)

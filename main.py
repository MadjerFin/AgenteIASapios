from fastapi import FastAPI
from pydantic import BaseModel
from core.agent import Agent
from services.audio_transcriber import transcrever_audio
from prompts.triagem import PROMPT_TRIAGEM
from prompts.mondial import PROMPT_MONDIAL
import base64
import tempfile
import json
import os

app = FastAPI(
    title="API Multi-Agentes",
    version="2.0.0",
    description="API com múltiplos agentes de IA independentes"
)

agent_triagem = Agent(prompt=PROMPT_TRIAGEM)
agent_mondial = Agent(prompt=PROMPT_MONDIAL)


# ================================
# MODELOS DE REQUEST
# ================================

class TextoRequest(BaseModel):
    mensagem: str


class AudioRequest(BaseModel):
    audio_base64: str
    formato: str


# ================================
# ROTAS BÁSICAS
# ================================

@app.get("/")
def home():
    return {
        "status": "API Multi-Agentes Online",
        "versao": "2.0.0",
        "agentes": ["triagem-veicular", "mondial"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# ================================
# AGENTE: TRIAGEM VEICULAR
# ================================

def _parse_triagem(texto: str) -> dict:
    try:
        return json.loads(texto)
    except Exception:
        return {
            "urgencia": 5,
            "problema_identificado": "Erro ao interpretar resposta",
            "acao_recomendada": "Encaminhar para humano",
            "pergunta_adicional": None,
            "resposta_bruta": texto
        }


@app.post("/triagem/texto")
def triagem_texto(request: TextoRequest):
    try:
        texto = agent_triagem.run(request.mensagem)
        return {"status": "sucesso", "analise": _parse_triagem(texto)}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}


@app.post("/triagem/audio")
def triagem_audio(request: AudioRequest):
    caminho_temp = None
    try:
        audio_bytes = base64.b64decode(request.audio_base64)

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{request.formato}") as tmp:
            tmp.write(audio_bytes)
            caminho_temp = tmp.name

        texto_transcrito = transcrever_audio(caminho_temp)
        texto = agent_triagem.run(texto_transcrito)

        return {
            "status": "sucesso",
            "transcricao": texto_transcrito,
            "analise": _parse_triagem(texto)
        }
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    finally:
        if caminho_temp and os.path.exists(caminho_temp):
            os.remove(caminho_temp)


# ================================
# AGENTE: MONDIAL (FRITADEIRA + VENTILADOR)
# ================================

@app.post("/mondial/texto")
def mondial_texto(request: TextoRequest):
    try:
        resposta = agent_mondial.run(request.mensagem)
        return {"status": "sucesso", "resposta": resposta}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}


@app.post("/mondial/audio")
def mondial_audio(request: AudioRequest):
    caminho_temp = None
    try:
        audio_bytes = base64.b64decode(request.audio_base64)

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{request.formato}") as tmp:
            tmp.write(audio_bytes)
            caminho_temp = tmp.name

        texto_transcrito = transcrever_audio(caminho_temp)
        resposta = agent_mondial.run(texto_transcrito)

        return {
            "status": "sucesso",
            "transcricao": texto_transcrito,
            "resposta": resposta
        }
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    finally:
        if caminho_temp and os.path.exists(caminho_temp):
            os.remove(caminho_temp)

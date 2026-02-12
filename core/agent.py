import os
import json
from google import genai
from dotenv import load_dotenv
from prompts.triagem import PROMPT_TRIAGEM

# Carrega variáveis do .env
load_dotenv()


class Agent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no .env")

        self.client = genai.Client(api_key=api_key)

    def run(self, mensagem):

        prompt_final = PROMPT_TRIAGEM + mensagem

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",  # removi -latest
            contents=prompt_final
        )

        texto = response.text.strip()

        try:
            return json.loads(texto)
        except Exception:
            return {
                "urgencia": "media",
                "problema_identificado": "Erro ao interpretar resposta",
                "risco": "Desconhecido",
                "acao_recomendada": "Encaminhar para humano",
                "perguntas_adicionais": [],
                "resposta_bruta": texto
            }

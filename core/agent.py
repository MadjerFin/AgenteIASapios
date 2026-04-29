import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


class Agent:
    def __init__(self, prompt: str):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no .env")

        self.client = genai.Client(api_key=api_key)
        self.prompt = prompt

    def run(self, mensagem: str) -> str:
        prompt_final = self.prompt + "\n\nMensagem do usuário:\n" + mensagem

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_final
        )

        return response.text.strip()

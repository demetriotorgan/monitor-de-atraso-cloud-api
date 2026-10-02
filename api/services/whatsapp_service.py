import os 
import httpx
from dotenv import load_dotenv

load_dotenv()

def enviar_mensagem(number: str, text:str):
    api_key = os.getenv("AUTHENTICATION_API_KEY")
    if not api_key:
        raise RuntimeError(
            "AUTHENTICATION_API_KEY não configurada"
        )
    url = "http://localhost:8080/message/sendText/Teste01"
    headers = {
        "apikey": api_key,
        "Content-Type":"application/json"
    }
    payload = {
        "number":number,
        "text":text
    }
    resposta = httpx.post(
        url,
        headers=headers,
        json=payload,
        timeout=10
    )
    
    resposta.raise_for_status()
    return resposta.json()

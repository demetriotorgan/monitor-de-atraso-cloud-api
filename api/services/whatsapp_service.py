import os
import httpx
from dotenv import load_dotenv

load_dotenv() # carrega seu .env

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

def enviar_whatsapp_template(telefone: str, responsavel: str, aluno_nome: str, data_hora: str, motivo: str):

    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        raise Exception("WHATSAPP_TOKEN ou WHATSAPP_PHONE_NUMBER_ID não encontrados no .env")

    url = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "template",
        "template": {
            "name": "aviso_atraso",
            "language": {"code": "pt_BR"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": responsavel},
                        {"type": "text", "text": aluno_nome},
                        {"type": "text", "text": data_hora},
                        {"type": "text", "text": motivo}
                    ]
                }
            ]
        }
    }

    with httpx.Client(timeout=30) as client:
        response = client.post(url, headers=headers, json=payload)
        print(f"[TEMPLATE] Status: {response.status_code} -> {response.text}")
        response.raise_for_status()
        return response.json()

# Mantém sua função antiga pra não quebrar nada
def enviar_mensagem(number: str, text: str):
    url = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {"body": text}
    }
    with httpx.Client(timeout=30) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
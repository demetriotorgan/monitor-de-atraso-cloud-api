import httpx
from fastapi import APIRouter, HTTPException
from models import TesteWhatsapp
from services.whatsapp_service import enviar_mensagem

router = APIRouter(prefix="/teste-whatsapp")

@router.post('/')
def testar_whatsapp(dados: TesteWhatsapp):
    try:
        resposta = enviar_mensagem(
            number= dados.number,
            text=dados.text
        )
        return {
            "message": "Mensagem enviada com sucesso!!",
            "evolution_response":resposta
        }
    except httpx.HTTPStatusError as erro:
        raise HTTPException(
            status_code=502,
            detail={
                'message':"A evolution API retornou um erro",
                'status_code':erro.response.status_code,
                'response': erro.response.text
            }
        )
    except httpx.RequestError as erro:
        raise HTTPException(
            status_code=502,
            detail=f'Não foi possível comunicar com o Evolution API: {erro}'
        )
    except RuntimeError as erro:
        raise HTTPException(
            status_code=500,
            detail=str(erro)
        )


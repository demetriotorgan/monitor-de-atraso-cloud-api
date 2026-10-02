from fastapi import APIRouter, HTTPException, status
from models import AtrasoCreate, AtrasoResponse, AtrasoUpdate
import httpx
from services.notificacao_service import reenviar_notificacao

from services.atraso_service import (
    registrar_atraso,
    listar_atrasos,
    buscar_atraso,
    excluir_atraso,
    atualizar_atraso,
    atualizar_parcialmente
)

from services.whatsapp_service import enviar_mensagem


router = APIRouter(prefix="/atrasos")

#---------ROta post--------
@router.post('/', response_model = AtrasoResponse, status_code=status.HTTP_201_CREATED)
def criar(atraso: AtrasoCreate):    
    try:
        #1-Criando registor de atraso 
        resultado = registrar_atraso(atraso)
        if resultado is None:
            raise HTTPException(
                status_code=404,
                detail="Aluno não encontrado"
            )        
        return {
            "id": resultado[0],
            "aluno_id": resultado[1],
            "data_hora": resultado[2],
            "motivo": resultado[3],
            "status_notificacao": resultado[4]
        }
        
    except HTTPException:
        raise        
    except (httpx.HTTPStatusError, httpx.RequestError):
        raise HTTPException(
            status_code=502,
            detail="Atraso registrado, mas não foi possível enviar a notificação"
        )
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao registrar atraso: {erro}"
        )

#---------Rota Get--------
@router.get('/', response_model=list[AtrasoResponse])
def listar():
    try:
        return listar_atrasos()
    
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao listar atrasos: {erro}'
        )
#---------Rota Get by ID--------
@router.get('/{id}', response_model=AtrasoResponse)
def buscar(id: int):
    try:
        return buscar_atraso(id)    
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar atraso: {erro}"
        )
                
#----------------Rota Delete by ID--------
@router.delete('/{id}')
def excluir(id:int):
    try:
        return excluir_atraso(id)
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao excluir atraso:{erro}'
        )
#--------ROTA PUT by ID-------------
@router.put("/{id}", response_model=AtrasoResponse)
def atualizar(id: int, atraso: AtrasoCreate):    
    try:
        return atualizar_atraso(id,atraso)         
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao atualizar atraso {erro}'
        )
#--------ROTA PATCH by ID-------------
@router.patch("/{id}", response_model=AtrasoResponse)
def atualizar_parcial(id:int , atraso: AtrasoUpdate):
    try:
        return atualizar_parcialmente(id, atraso)        
        
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao atualizar parcialmente o atraso: {erro}'
        )
#---Rota Retry-----
@router.post("/{id}/reenviar", response_model=AtrasoResponse)
def reenviar(id: int):
    try:
        return reenviar_notificacao(id)

    except HTTPException:
        raise

    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao reenviar notificação: {erro}"
        )

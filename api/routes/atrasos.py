from fastapi import APIRouter, HTTPException, status
from models import AtrasoCreate, AtrasoResponse, AtrasoUpdate
from services.time_service import converter_para_brasilia


from services.notificacao_service import reenviar_notificacao, NotificacaoError
from services.atraso_service import (
    registrar_atraso,
    listar_atrasos,
    buscar_atraso,
    excluir_atraso,
    atualizar_atraso,
    atualizar_parcialmente
)

router = APIRouter(prefix="/atrasos", tags=["Atrasos"])

#---------ROTA POST--------
@router.post('/', response_model=AtrasoResponse, status_code=status.HTTP_201_CREATED)
def criar(atraso: AtrasoCreate):
    try:
        resultado = registrar_atraso(atraso) # já envia template e atualiza status

        if resultado is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")

        # resultado é uma tupla: (id, aluno_id, data_hora, motivo, status)
        return {
            "id": resultado[0],
            "aluno_id": resultado[1],
            "data_hora": converter_para_brasilia(resultado[2]),
            "motivo": resultado[3],
            "status_notificacao": resultado[4]
        }

    except HTTPException:
        raise
    except Exception as erro:
        print(f"[ERRO /atrasos POST] {erro}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao registrar atraso: {erro}"
        )

#---------ROTA GET--------
@router.get('/', response_model=list[AtrasoResponse])
def listar():
    try:
        return listar_atrasos()
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f'Erro ao listar atrasos: {erro}')

#---------ROTA GET BY ID--------
@router.get('/{id}', response_model=AtrasoResponse)
def buscar(id: int):
    try:
        resultado = buscar_atraso(id)
        if resultado is None:
            raise HTTPException(status_code=404, detail="Atraso não encontrado")
        return resultado
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar atraso: {erro}")

#---------ROTA DELETE--------
@router.delete('/{id}')
def excluir(id: int):
    try:
        return excluir_atraso(id)
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f'Erro ao excluir atraso: {erro}')

#---------ROTA PUT--------
@router.put("/{id}", response_model=AtrasoResponse)
def atualizar(id: int, atraso: AtrasoCreate):
    try:
        return atualizar_atraso(id, atraso)
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f'Erro ao atualizar atraso {erro}')

#---------ROTA PATCH--------
@router.patch("/{id}", response_model=AtrasoResponse)
def atualizar_parcial(id: int, atraso: AtrasoUpdate):
    try:
        return atualizar_parcialmente(id, atraso)
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f'Erro ao atualizar parcialmente: {erro}')

#---------ROTA RETRY (REENVIO COM TEMPLATE)--------
@router.post("/{id}/reenviar", response_model=AtrasoResponse)
def reenviar(id: int):
    try:
        registro = reenviar_notificacao(id) # agora usa template
        if registro is None:
            raise HTTPException(status_code=404, detail="Atraso não encontrado")

        return {
            "id": registro[0],
            "aluno_id": registro[1],
            "data_hora": converter_para_brasilia(registro[2]),
            "motivo": registro[3],
            "status_notificacao": registro[4]
        }
    except HTTPException:
        raise
    except NotificacaoError as erro:
        print(f"[ERRO META] {erro}")
        raise HTTPException(
            status_code=502,
            detail={
                "mensagem": erro.mensagem,
                "erro_meta":{
                    "status": erro.status_meta,
                    "codigo": erro.codigo_meta,
                    "mensagem": erro.mensagem_meta,
                    "tipo": erro.tipo_meta,
                    "detalhe": erro.detalhe_meta,
                    "fbtrace_id": erro.fbtrace_id
                }
            }
        )
    except Exception as erro:
        print(f"[ERRO REENVIO] {erro}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao reenviar notificação: {erro}"
        )
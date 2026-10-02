from fastapi import APIRouter, HTTPException, Query, status
from models import AlunoCreate, AlunoResponse,AlunoUpdate
from services.aluno_service import (
    criar_aluno,
    listar_alunos,
    excluir_aluno,
    atualizar_aluno,
    atualizar_parcialmente    
    )



router = APIRouter(prefix="/alunos")

@router.post(
    "/",
    response_model=AlunoResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar(aluno:AlunoCreate):
    try:
        registro = criar_aluno(
            nome = aluno.nome,
            serie = aluno.serie,
            responsavel= aluno.responsavel,
            telefone_responsavel=aluno.telefone_responsavel
        )
        return{
            "id":registro[0],
            "nome":registro[1],
            "serie":registro[2],
            "responsavel":registro[3],
            "telefone_responsavel":registro[4]
        }
    
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao cadastrar aluno: {erro}'
        )

@router.get('/', response_model=list[AlunoResponse])
def listar(nome:str | None = Query(default=None)):
    try:
        registros = listar_alunos(nome)
        return [
            {
                "id":registro[0],
                "nome":registro[1],
                "serie":registro[2],
                "responsavel":registro[3],
                "telefone_responsavel":registro[4]
            }
            for registro in registros
        ]
    
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar alunos:{erro}"
        )

#---Rota Delete by ID----------
@router.delete('/{id}')
def excluir(id:int):
    try:
        return excluir_aluno(id)
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao excluir atraso:{erro}'
        )

#---Rota PUT
@router.put("/{id}", response_model=AlunoResponse)
def atualizar(id:int, aluno:AlunoCreate):
    try:
        return atualizar_aluno(id, aluno)
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao atualizar aluno {erro}'
        )

#--- Rota Patch
@router.patch("/{id}", response_model=AlunoResponse)
def atualizar_parcial(id:int, aluno:AlunoUpdate):
    try:
        return atualizar_parcialmente(id, aluno)
    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao atualizar parcialmente aluno: {erro}'
        )
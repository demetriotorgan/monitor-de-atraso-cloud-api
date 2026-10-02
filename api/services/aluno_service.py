from fastapi import HTTPException
from database import get_connection
from models import AlunoCreate,AlunoUpdate

def criar_aluno(nome, serie, responsavel, telefone_responsavel):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO alunos(
                    nome,
                    serie,
                    responsavel,
                    telefone_responsavel
                )
                VALUES (%s, %s, %s,%s)
                RETURNING
                    id,
                    nome,
                    serie,
                    responsavel,
                    telefone_responsavel
                """,
                (nome,
                 serie,
                 responsavel,
                 telefone_responsavel
                 )
            )
            registro = cursor.fetchone()
    return registro

#---BUSCA POR NOME---
def listar_alunos(nome=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            if nome:                
                cursor.execute(
                    """
                    SELECT id, nome, serie, responsavel, telefone_responsavel
                    FROM alunos
                    WHERE nome ILIKE %s
                    ORDER BY id
                    """,
                    (f"%{nome}%",)
                )
            else:
                cursor.execute(
                    """
                    SELECT
                        id,
                        nome,
                        serie,
                        responsavel,
                        telefone_responsavel
                    FROM alunos
                    ORDER BY id
                    """
                )
            registros = cursor.fetchall()
    return registros  

#---BUSCA POR ID---
def buscar_aluno(id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
            """
            SELECT id, nome, serie, responsavel, telefone_responsavel
            FROM alunos
            WHERE id = %s
            """,
            (id,)
            )
            registro = cursor.fetchone()
    return registro

#---Exclur aluno-----
def excluir_aluno(id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM alunos
                WHERE id = %s
                """,
                (id,)
            )
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail='Aluno não encontrado'
                )
    return{
        'message':'Aluno excluído com sucesso!'
    }
    
#------PUT--------
def atualizar_aluno(id:int, aluno:AlunoCreate):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE alunos
                SET
                    nome =  %s,
                    serie = %s,
                    responsavel = %s,
                    telefone_responsavel = %s
                WHERE id = %s
                RETURNING id,nome, serie, responsavel, telefone_responsavel
                """,
                    (aluno.nome, aluno.serie, aluno.responsavel, aluno.telefone_responsavel, id)
            )
            registro = cursor.fetchone()
        if registro is None:
            raise HTTPException(
                status_code=404,
                detail='Aluno não encontrado'
            )
    return{       
        "id": registro[0],
        "nome": registro[1],
        "serie": registro[2],
        "responsavel": registro[3],
        "telefone_responsavel": registro[4]
    }
    
#------Patch    
def atualizar_parcialmente(id:int, aluno:AlunoUpdate):
    dados = aluno.model_dump(exclude_unset=True)
    if not dados:
        raise HTTPException(
            status_code=400,
            detail='Nenhum campo informado para atualização'
        )
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nome, serie, responsavel, telefone_responsavel
                FROM alunos
                WHERE id = %s                
                """,
                (id,)
            )
            registro = cursor.fetchone()
            if registro is None:
                raise HTTPException(
                    status_code=404,
                    detail='Registro não encontrado'
                )
            nome = dados.get('nome', registro[1])
            serie=dados.get('serie', registro[2])
            responsavel=dados.get('responsavel', registro[3])
            telefone_responsavel=dados.get('telefone_responsavel', registro[4])
            
            cursor.execute(
                """
                UPDATE alunos
                    SET
                        nome = %s,
                        serie=%s,
                        responsavel=%s,
                        telefone_responsavel=%s
                    WHERE id = %s
                    RETURNING id, nome, serie, responsavel, telefone_responsavel
                """,
                (nome, serie, responsavel, telefone_responsavel, id)
            )
            registro = cursor.fetchone()
    return{
        "id":registro[0],
        "nome":registro[1],
        "serie":registro[2],
        "responsavel":registro[3],
        "telefone_responsavel":registro[4]
    }
from fastapi import  HTTPException
from models import AtrasoCreate, AtrasoUpdate
from database import get_connection
from services.aluno_service import buscar_aluno
from services.whatsapp_service import enviar_mensagem
import httpx


def criar_atraso(atraso: AtrasoCreate):
    aluno = buscar_aluno(atraso.aluno_id)
    if aluno is None:
        return None
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO atrasos(
                    aluno_id,
                    data_hora,
                    motivo
                )
                VALUES(%s, CURRENT_TIMESTAMP,%s)   
                RETURNING id, aluno_id, data_hora, motivo,status_notificacao    
                """,
                (atraso.aluno_id, atraso.motivo)
            )
            registro = cursor.fetchone()
        return {
            "atraso": registro,
             "aluno": aluno
        }
#----Atualiza status de envio-----
def atualizar_status_notificacao(id: int, status: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE atrasos
                SET status_notificacao = %s
                WHERE id = %s
                RETURNING id, aluno_id, data_hora, motivo, status_notificacao
            """, (status, id))

            registro = cursor.fetchone()

            if registro is None:
                raise HTTPException(
                    status_code=404,
                    detail="Atraso não encontrado"
                )

    return registro
#-----registrar atraso----------
def registrar_atraso(atraso: AtrasoCreate):
    resultado = criar_atraso(atraso)

    if resultado is None:
        return None

    registro = resultado["atraso"]
    aluno = resultado["aluno"]

    texto = f"""
📚 Monitor de Atraso — Registro de Chegada
Olá, {aluno[3]}! 👋
Informamos que o(a) aluno(a) {aluno[1]} chegou à escola após o horário previsto.

    🕐 Data e horário: {registro[2].strftime("%d/%m/%Y às %H:%M")}
    📌 Motivo informado: {registro[3]}

O registro foi realizado pela equipe escolar.
Agradecemos a atenção e a parceria! 🤝

🏫 Monitor de Atraso - Colégio Ary João Dresch
"""
    try:    
        enviar_mensagem(
            number=aluno[4],
            text=texto
        )
        
        registro = atualizar_status_notificacao(
        id=registro[0],
        status="ENVIADA"
        )
    except (httpx.HTTPStatusError, httpx.RequestError):
        registro = atualizar_status_notificacao(id=registro[0], status="FALHOU")
        raise

    return registro


#----------GET--------------
def listar_atrasos():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, motivo, aluno_id, data_hora, status_notificacao
                FROM atrasos
                ORDER BY id                    
                """
            )
            registros = cursor.fetchall()
    return[
        {
            "id":registro[0],
            "motivo":registro[1],
            "aluno_id": registro[2],
            "data_hora":registro[3],
            "status_notificacao": registro[4]
        }
        for registro in registros
    ]
    

def buscar_atraso(id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, motivo, aluno_id, data_hora
                FROM atrasos
                WHERE id = %s
                """,
                (id,)
            )
            registro = cursor.fetchone()
    if registro is None:
        raise HTTPException(
            status_code=404,
            detail='Atraso não encontrado'
        )
    return {
        "id":registro[0],
        "motivo":registro[1],
        "aluno_id":registro[2],
        "data_hora":registro[3]
    }
    

#----------DELETE------------
def excluir_atraso(id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM atrasos
                WHERE id = %s
                """,
                (id,)
            )
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail='Atraso não encontrado'
                )
    return{
        'message':'Atraso excluído com sucesso!'
    }             

#---------PUT--------
def atualizar_atraso(id: int, atraso: AtrasoCreate):    
    aluno = buscar_aluno(atraso.aluno_id)
    if aluno is None:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
            """
            UPDATE atrasos
            SET 
                aluno_id= %s,               
                motivo = %s,
                data_hora = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, aluno_id, data_hora, motivo
            """,
                (atraso.aluno_id,atraso.motivo,id)
            )
            registro = cursor.fetchone()
        if registro is None:
            raise HTTPException(
                status_code=404,
                detail='Atraso não encontrado'
            )
    return{
        "id":registro[0],
        "aluno_id":registro[1],
        "data_hora":registro[2],
        "motivo":registro[3]
    }

#-----------PATCH-------
def atualizar_parcialmente(id: int, atraso:AtrasoUpdate):
    dados = atraso.model_dump(exclude_unset=True)
    if not dados:
        raise HTTPException(
            status_code=400,
            detail='Nenhum campo informado para atualização'
        )
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, aluno_id, data_hora, motivo
                FROM atrasos
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
            aluno_id = dados.get('aluno_id', registro[1])
            motivo = dados.get('motivo', registro[3])
            
            aluno = buscar_aluno(aluno_id)
            if aluno is None:
                raise HTTPException(
                    status_code=404,
                    detail="Aluno não encontrado"
                )
            
            cursor.execute(
                """
                UPDATE atrasos
                SET
                    aluno_id=%s,
                    motivo=%s
                WHERE id = %s
                RETURNING id, aluno_id, data_hora, motivo
                """,
                (aluno_id, motivo,id)
            )
            registro = cursor.fetchone()
    return {
        "id":registro[0],
        "aluno_id":registro[1],
        "data_hora":registro[2],
        "motivo":registro[3]
    } 
   
    
 
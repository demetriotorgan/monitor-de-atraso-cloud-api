from fastapi import HTTPException
from services.whatsapp_service import enviar_mensagem
from database import get_connection
from services.aluno_service import buscar_aluno
import httpx


def buscar_dados_notificacao(id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, aluno_id, data_hora, motivo, status_notificacao
                FROM atrasos
                WHERE id = %s
            """, (id,))

            atraso = cursor.fetchone()

    if atraso is None:
        raise HTTPException(
            status_code=404,
            detail="Atraso não encontrado"
        )

    aluno = buscar_aluno(atraso[1])

    if aluno is None:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    return {
        "atraso": atraso,
        "aluno": aluno
    }
    
#----Reenvio----
def reenviar_notificacao(id: int):
    dados = buscar_dados_notificacao(id)

    atraso = dados["atraso"]
    aluno = dados["aluno"]

    if atraso[4] != "FALHOU":
        raise HTTPException(
            status_code=400,
            detail="Atraso não possui notificação com falha"
        )

    texto = f"""
📚 Monitor de Atraso — Registro de Chegada
Olá, {aluno[3]}! 👋
Informamos que o(a) aluno(a) {aluno[1]} chegou à escola após o horário previsto.

    🕐 Data e horário: {atraso[2].strftime("%d/%m/%Y às %H:%M")}
    📌 Motivo informado: {atraso[3]}

O registro foi realizado pela equipe escolar.
Agradecemos a atenção e a parceria! 🤝

🏫 Monitor de Atraso - Colégio Ary João Dresch
"""

    try:
        enviar_mensagem(
            number=aluno[4],
            text=texto
        )

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE atrasos
                    SET status_notificacao = 'ENVIADA'
                    WHERE id = %s
                    RETURNING id, aluno_id, data_hora, motivo, status_notificacao
                """, (id,))

                registro = cursor.fetchone()

        return registro

    except (httpx.HTTPStatusError, httpx.RequestError):
        raise HTTPException(
            status_code=502,
            detail="Não foi possível reenviar a notificação."
        )
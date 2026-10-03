from fastapi import HTTPException
from services.whatsapp_service import enviar_whatsapp_template # MUDOU AQUI
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
        raise HTTPException(status_code=404, detail="Atraso não encontrado")

    aluno = buscar_aluno(atraso[1])

    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    return {"atraso": atraso, "aluno": aluno}

#----Reenvio----
def reenviar_notificacao(id: int):
    dados = buscar_dados_notificacao(id)

    atraso = dados["atraso"] # [id, aluno_id, data_hora, motivo, status]
    aluno = dados["aluno"] # [id, nome, turma, responsavel, telefone_responsavel...]

    if atraso[4]!= "FALHOU":
        raise HTTPException(
            status_code=400,
            detail="Atraso não possui notificação com falha"
        )

    # Dados para o template aviso_atraso
    responsavel = aluno[3]
    aluno_nome = aluno[1]
    telefone = aluno[4]
    motivo = atraso[3]
    data_formatada = atraso[2].strftime("%d/%m/%Y às %H:%M")

    try:
        # AGORA USANDO TEMPLATE OFICIAL
        enviar_whatsapp_template(
            telefone=telefone,
            responsavel=responsavel,
            aluno_nome=aluno_nome,
            data_hora=data_formatada,
            motivo=motivo
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

    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        print(f"Erro no reenvio template: {e}")
        raise HTTPException(
            status_code=502,
            detail="Não foi possível reenviar a notificação."
        )
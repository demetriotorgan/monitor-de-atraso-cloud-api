import psycopg
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:MonitorAtraso2026Forte!@db:5432/monitor_atraso")

SQL = """
CREATE TABLE IF NOT EXISTS alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR NOT NULL,
    serie VARCHAR NOT NULL,
    responsavel VARCHAR NOT NULL,
    telefone_responsavel VARCHAR NOT NULL
);
CREATE TABLE IF NOT EXISTS atrasos (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    data_hora TIMESTAMP NOT NULL DEFAULT NOW(),
    motivo TEXT NOT NULL,
    status_notificacao VARCHAR NOT NULL DEFAULT 'pendente'
);
"""

def init_db():
    for i in range(15):
        try:
            conn = psycopg.connect(DATABASE_URL)
            conn.execute(SQL)
            conn.commit()
            conn.close()
            print("✅ Tabelas verificadas/criadas")
            return
        except Exception as e:
            print(f"⏳ DB ainda não pronto ({i+1}/15): {e}")
            time.sleep(2)
    print("❌ Falha ao criar tabelas")
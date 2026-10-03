#iniciar venv: source /home/demetrio/monitor-atraso/api/.venv/bin/activate
#iniciar aplicação: uvicorn main:app --reload
#iniciar psql: docker exec -it monitor-postgres psql -U postgres -d monitor_atraso
#ver logs: docker compose logs -f

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.atrasos import router as atrasos_router
from routes.whatsapp import router as whatsapp_router
from routes.alunos import router as alunos_router

app = FastAPI(
    title="Monitor de Atraso API",
    version="1.0.0"
)

# Libera o frontend pra chamar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # em produção troca pelo domínio do Colégio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(atrasos_router)
app.include_router(whatsapp_router)
app.include_router(alunos_router)

#Rota root
@app.get('/')
def root():
    return {'mensagem': 'Monitor de Atraso API - Online'}

#Rota Status
@app.get("/status")
def status():
    return {
        "status": "online",
        "service": "Monitor de Atraso API"
    }
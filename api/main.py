#inicar venv: source /home/demetrio/monitor-atraso/api/.venv/bin/activate
#iniciar aplicação: uvicorn main:app --reload
#iniciar psql:  docker exec -it evolution-postgres psql -U evolution -d evolution

from fastapi import FastAPI
from routes.atrasos import router as atrasos_router
from routes.whatsapp import router as whatsapp_router
from routes.alunos import router as alunos_router

app = FastAPI()
app.include_router(atrasos_router)
app.include_router(whatsapp_router)
app.include_router(alunos_router)



#Rota root
@app.get('/')
def root():
    return {'messagem' : 'Monitor de atraso API'}

#Rota Status
@app.get("/status")
def status():
    return {
                "status":"online",
                "service":"Monitor de Atraso API"
            }

from fastapi import FastAPI
from app.routes import diagnostico_routes

app = FastAPI(title="API Diagnóstico de Fallas Mecánicas")

app.include_router(diagnostico_routes.router, prefix="/diagnostico")

@app.get("/")
def root():
    return {"mensaje": "API de diagnóstico mecánico funcionando correctamente"}

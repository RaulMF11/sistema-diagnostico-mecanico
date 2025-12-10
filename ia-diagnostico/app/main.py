from fastapi import FastAPI
from app.routes.diagnostico_routes import router as diagnostico_router

app = FastAPI(title="API Diagnóstico de Fallas Mecánicas")

app.include_router(diagnostico_router, prefix="/diagnostico", tags=["Diagnóstico"])

@app.get("/")
def root():
    return {"status": "ok", "mensaje": "API Diagnóstico IA funcionando"}

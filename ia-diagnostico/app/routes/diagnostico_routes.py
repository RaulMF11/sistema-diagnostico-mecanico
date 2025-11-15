# app/routes/diagnostico_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.model.model_handler import cargar_modelo, predecir_caso

router = APIRouter(tags=["Diagnóstico"])

# Esquema de entrada (campos opcionales y descripción obligatoria)
class DescripcionEntrada(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anio: Optional[int] = None
    km: Optional[int] = None
    rpm: Optional[int] = None
    presion_aceite: Optional[float] = None
    temperatura_motor: Optional[float] = None
    descripcion: str

# Carga el modelo solo una vez al iniciar la API
modelo, preprocessor = cargar_modelo()

@router.post("/")
def diagnosticar_falla(entrada: DescripcionEntrada):
    """
    Endpoint principal para diagnóstico.
    Recibe datos del vehículo y una descripción textual del problema.
    """
    try:
        prediccion = predecir_caso(modelo, preprocessor, entrada.dict())
        return {"resultado": prediccion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

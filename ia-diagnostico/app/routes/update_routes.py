from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

router = APIRouter(prefix="/actualizar", tags=["Retraining"])

class NuevoCaso(BaseModel):
    marca: str
    modelo: str
    anio: int
    km: int
    ultimo_mantenimiento: int
    presion_aceite: float
    rpm: int
    temperatura_motor: float
    descripcion: str
    falla: str

@router.post("/registrar")
def registrar_nuevo_caso(caso: NuevoCaso):
    ruta_archivo = os.path.join("data", "nuevos_casos.csv")
    df_nuevo = pd.DataFrame([caso.dict()])

    # Crear el archivo si no existe
    if not os.path.exists(ruta_archivo):
        df_nuevo.to_csv(ruta_archivo, index=False)
    else:
        df_existente = pd.read_csv(ruta_archivo)
        df_actualizado = pd.concat([df_existente, df_nuevo], ignore_index=True)
        df_actualizado.to_csv(ruta_archivo, index=False)

    return {"mensaje": "✅ Nuevo caso registrado para retraining", "data": caso}

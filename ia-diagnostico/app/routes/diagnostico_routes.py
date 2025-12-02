from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional
# IMPORTACIÓN CORREGIDA: Usamos el alias para acceder al módulo
import app.model.model_handler as modelo_handler 

router = APIRouter()

# Variable global privada para almacenar la instancia del servicio ML.
# Se inicializa a None y se carga bajo demanda.
_servicio_ml_instance = None

def get_servicio_ml():
    """
    Carga perezosa del ModeloServicio.
    Intenta cargar los recursos solo una vez.
    """
    global _servicio_ml_instance
    
    # Si el servicio ya está cargado, devolverlo
    if _servicio_ml_instance is not None:
        return _servicio_ml_instance
        
    # Si no está cargado, intentar cargarlo
    try:
        _servicio_ml_instance = modelo_handler.cargar_recursos()
        print("INFO: Servicio ML cargado exitosamente.")
        return _servicio_ml_instance
    except FileNotFoundError as e:
        # En caso de que los archivos .pkl no existan, lanzamos una excepción HTTP.
        print(f"ADVERTENCIA: El modelo no se pudo cargar. Error: {e}")
        # Notar que ya no se asigna 'servicio = None' globalmente, 
        # sino que se lanza la excepción que será capturada por la ruta.
        raise HTTPException(status_code=503, detail="El servicio de ML no está disponible. Entrena el modelo primero con 'python -m app.model.train_model'.")
    except AttributeError as e:
        # Esto captura el error exacto que ocurre al fallar la carga en Uvicorn.
        # Elevamos a un error 500 que aconseja reintentar o verificar dependencias.
        print(f"ERROR INTERNO: Fallo al cargar el recurso. Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno al inicializar el servicio: {str(e)}. Intenta reiniciar Uvicorn.")


class DiagnosticoInput(BaseModel):
    # Campos obligatorios o fuertemente recomendados
    marca: Optional[str] = Field(None, description="Marca del vehículo")
    modelo: Optional[str] = Field(None, description="Modelo del vehículo")
    anio: Optional[int] = Field(None, description="Año de fabricación (e.g., 2017)")
    kilometraje: Optional[float] = Field(None, description="Kilometraje actual")
    ultimo_mantenimiento: Optional[str] = Field(None, description="Fecha del último mantenimiento (YYYY-MM-DD)")
    descripcion_sintomas: str = Field(..., description="Descripción detallada de los síntomas de la falla")
    
    # Campos opcionales (sensores)
    rpm: Optional[float] = Field(None, description="Revoluciones por minuto")
    presion_aceite: Optional[float] = Field(None, description="Presión de aceite (e.g., psi)")
    temperatura_motor: Optional[float] = Field(None, description="Temperatura del motor (°C)")
    nivel_combustible: Optional[float] = Field(None, description="Nivel de combustible (%)")
    voltaje_bateria: Optional[float] = Field(None, description="Voltaje de la batería (e.g., 12.5)")
    velocidad: Optional[float] = Field(None, description="Velocidad actual (km/h)")
    
# ================================
#   📌 RUTA PARA ENTRENAR MODELO
# ================================
# ----------- ENDPOINT PARA ENTRENAR ------------------
@router.post("/entrenar", summary="Entrena el modelo en background")
def entrenar_modelo(background: BackgroundTasks):
    background.add_task(modelo_handler.entrenar_modelo)

    return {
        "status": "ok",
        "mensaje": "Entrenamiento iniciado en segundo plano. Esto puede tardar 1–3 minutos."
    }

@router.post("/", summary="Realiza diagnóstico a partir de los datos")
def diagnosticar(payload: DiagnosticoInput, servicio=Depends(get_servicio_ml)):
    # NOTA: El argumento 'servicio' ahora recibe la instancia cargada gracias a Depends(get_servicio_ml)
    try:
        # Convertir el payload a diccionario
        # Exclude_none=True elimina los campos que el usuario no envió
        data = payload.dict(exclude_none=True) 
        
        # Accedemos al método predecir a través de la instancia del servicio
        resultado = servicio.predecir(data)
        return {"input": data, "resultado": resultado}
    except Exception as e:
        # Manejo de errores durante la predicción
        print(f"Error durante la predicción: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del modelo durante la predicción: {str(e)}")
    
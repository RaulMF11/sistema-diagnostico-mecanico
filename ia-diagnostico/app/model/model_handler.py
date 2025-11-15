import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict

MODEL_PATH = os.path.join(os.path.dirname(__file__), "modelo.pkl")
PREPROCESSOR_PATH = os.path.join(os.path.dirname(__file__), "preprocessor.pkl")

def cargar_modelo():
    """
    Carga y devuelve (modelo, preprocessor).
    """
    if not os.path.exists(MODEL_PATH) or not os.path.exists(PREPROCESSOR_PATH):
        raise FileNotFoundError("Modelo o preprocessor no encontrado. Entrena primero con training/train_model.py")

    modelo = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    return modelo, preprocessor

def predecir_caso(modelo, preprocessor, entrada: Dict):
    """
    Entrada: dict con keys: marca, modelo, anio, km, rpm, presion_aceite, temperatura_motor, descripcion
    Retorna etiqueta predicha.
    """
    # Crear DataFrame de 1 fila con las columnas esperadas
    df = pd.DataFrame([{
        "marca": entrada.get("marca", None),
        "modelo": entrada.get("modelo", None),
        "anio": entrada.get("anio", None),
        "km": entrada.get("km", None),
        "rpm": entrada.get("rpm", None),
        "presion_aceite": entrada.get("presion_aceite", None),
        "temperatura_motor": entrada.get("temperatura_motor", None),
        "descripcion": entrada.get("descripcion", "")
    }])

    # Transformar con el preprocessor cargado
    X = preprocessor.transform(df)
    pred = modelo.predict(X)[0]

    # si el modelo soporta predict_proba:
    prob = None
    if hasattr(modelo, "predict_proba"):
        prob = modelo.predict_proba(X).max()

    return {"falla": str(pred), "probabilidad": float(prob) if prob is not None else None}

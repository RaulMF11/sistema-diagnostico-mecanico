import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from app.utils.helpers import preprocesar_datos

DATA_PATH = os.path.join("data", "dataset.csv")
NEW_PATH = os.path.join("data", "nuevos_casos.csv")
MODEL_DIR = os.path.join("app", "model")
MODEL_PATH = os.path.join(MODEL_DIR, "modelo.pkl")
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, "preprocessor.pkl")

def update_model():
    print("🔁 Ejecutando reentrenamiento por lote...")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"No se encontró el dataset en {DATA_PATH}")

    df_base = pd.read_csv(DATA_PATH)
    if os.path.exists(NEW_PATH):
        df_nuevos = pd.read_csv(NEW_PATH)
        df_total = pd.concat([df_base, df_nuevos], ignore_index=True)
    else:
        df_total = df_base

    if "falla" not in df_total.columns:
        raise ValueError("Los datos combinados deben contener la columna 'falla'.")

    X, y, preprocessor = preprocesar_datos(df_total)

    model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
    model.fit(X, y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)

    # Reemplazar dataset principal por combinado
    df_total.to_csv(DATA_PATH, index=False)

    # Eliminar o limpiar nuevos_casos
    if os.path.exists(NEW_PATH):
        os.remove(NEW_PATH)

    print(f"✅ Modelo actualizado y guardado en {MODEL_PATH}. Total registros: {len(df_total)}")

if __name__ == "__main__":
    update_model()

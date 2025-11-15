import os
import sys
# Añadir carpeta raíz al path para importar el paquete app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from app.utils.helpers import preprocesar_datos

# Rutas
DATA_PATH = os.path.join("data", "dataset.csv")
MODEL_DIR = os.path.join("app", "model")
MODEL_PATH = os.path.join(MODEL_DIR, "modelo.pkl")
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, "preprocessor.pkl")

def entrenar_modelo():
    print("🚀 Iniciando entrenamiento del modelo...")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"No se encontró el dataset en {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    if "falla" not in df.columns:
        raise ValueError("El dataset debe contener una columna llamada 'falla'.")

    X, y, preprocessor = preprocesar_datos(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n📊 Reporte de evaluación:")
    print(classification_report(y_test, y_pred))
    print(f"✅ Precisión general: {accuracy_score(y_test, y_pred):.2%}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)

    print(f"\n💾 Modelo guardado en: {MODEL_PATH}")
    print(f"💾 Preprocesador guardado en: {PREPROCESSOR_PATH}")
    print("🎯 Entrenamiento completado exitosamente.")

if __name__ == "__main__":
    entrenar_modelo()

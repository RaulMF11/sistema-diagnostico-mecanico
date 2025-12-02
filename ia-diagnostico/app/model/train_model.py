"""
Script de entrenamiento. Ejecutar desde la raíz del proyecto:
(venv) $ python -m app.model.train_model
"""
import os
import sys
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# --- FIX IMPORTANTE PARA RAILWAY ---
# Asegurar que la raíz del proyecto esté en sys.path
# Detectar ruta real de ROOT en Railway
CURRENT_FILE = os.path.abspath(__file__)
MODEL_DIR = os.path.dirname(CURRENT_FILE)               # /app/app/model
APP_DIR = os.path.dirname(MODEL_DIR)                   # /app/app
ROOT_DIR = os.path.dirname(APP_DIR)                    # /app   ← REAL ROOT

# Agregar ambos al sys.path por seguridad
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

print("DEBUG PATHS:")
print("MODEL_DIR:", MODEL_DIR)
print("APP_DIR:", APP_DIR)
print("ROOT_DIR:", ROOT_DIR)

# Ahora sí importa correctamente
from app.model.preprocess import fit_transform_all, BASE_DIR, load_label_encoders

# Guardar el modelo en la carpeta del script
MODEL_PATH = os.path.join(MODEL_DIR, "modelo_multioutput.pkl")
os.makedirs(MODEL_DIR, exist_ok=True)

def entrenar():
    print("📌 Entrenando: cargando y transformando datos...")
    X, y = fit_transform_all(csv_path="dataset.csv", save_artifacts=True)

    print(f"Datos cargados. X shape: {X.shape}, Y shape: {y.shape}")

    print("📌 Dividiendo dataset (80% Train, 20% Test)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("📌 Configurando modelo MultiOutput (RandomForest)...")
    base_clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    modelo = MultiOutputClassifier(estimator=base_clf, n_jobs=-1)

    print("📌 Entrenando modelo...")
    modelo.fit(X_train, y_train)
    
    print("📌 Evaluando modelo...")
    y_pred = modelo.predict(X_test)

    encs = load_label_encoders()

    target_map = {
        0: {"col_name": "falla_principal", "enc_key": "falla"}, 
        1: {"col_name": "subfalla", "enc_key": "subfalla"}, 
        2: {"col_name": "nivel_gravedad", "enc_key": "gravedad"},
        3: {"col_name": "posibles_soluciones", "enc_key": "solucion"}
    }

    for i, config in target_map.items():
        enc_key = config["enc_key"]
        name = config["col_name"]
        labels_real = encs[enc_key].inverse_transform(y_test[:, i])
        labels_pred = encs[enc_key].inverse_transform(y_pred[:, i])

        print(f"\n--- Reporte de Clasificación para: {name} ---")
        print(classification_report(labels_real, labels_pred, zero_division=0))

    print("📌 Guardando modelo en:", MODEL_PATH)
    joblib.dump(modelo, MODEL_PATH)
    print("✅ Entrenamiento finalizado y modelo guardado.")

if __name__ == "__main__":
    entrenar()

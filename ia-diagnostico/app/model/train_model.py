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
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from app.model.preprocess import fit_transform_all, BASE_DIR, load_label_encoders

# Path donde se guardará el modelo entrenado
MODEL_PATH = os.path.join(BASE_DIR, "modelo_multioutput.pkl")

def entrenar():
    os.makedirs(BASE_DIR, exist_ok=True) 

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

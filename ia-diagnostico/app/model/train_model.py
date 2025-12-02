"""
Script de entrenamiento. Ejecutar desde la raíz del proyecto:
(venv) $ python -m app.model.train_model
"""
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
# Importar fit_transform_all desde preprocess.py
from app.model.preprocess import fit_transform_all, BASE_DIR, load_label_encoders
from sklearn.calibration import CalibratedClassifierCV

# Path donde se guardará el modelo entrenado
MODEL_PATH = os.path.join(BASE_DIR, "modelo_multioutput.pkl")

def entrenar():
    # Asegurar que el directorio app/model exista
    os.makedirs(BASE_DIR, exist_ok=True) 

    print("📌 Entrenando: cargando y transformando datos...")
    # csv_path apunta a dataset.csv en la raíz del proyecto
    X, y = fit_transform_all(csv_path="dataset.csv", save_artifacts=True)

    print(f"Datos cargados. X shape: {X.shape}, Y shape: {y.shape}")

    print("📌 Dividiendo dataset (80% Train, 20% Test)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("📌 Configurando modelo MultiOutput (RandomForest)...")
    # Base Estimator: RandomForest con 200 árboles
    base_clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    # Envolver para clasificación multi-salida
    modelo = MultiOutputClassifier(estimator=base_clf, n_jobs=-1)

    print("📌 Entrenando modelo (esto puede tardar un momento)...")
    modelo.fit(X_train, y_train)
    
    print("📌 Evaluando modelo en el conjunto de prueba...")
    y_pred = modelo.predict(X_test)
    
    # Cargar los LabelEncoders para decodificar los nombres de las clases
    encs = load_label_encoders()
    
    # Mapeo de índices de salida a las claves reales del diccionario 'encs'
    # Esto corrige el KeyError 'nivel' -> 'gravedad'
    target_map = {
        0: {"col_name": "falla_principal", "enc_key": "falla"}, 
        1: {"col_name": "subfalla", "enc_key": "subfalla"}, 
        2: {"col_name": "nivel_gravedad", "enc_key": "gravedad"}, # CLAVE CORREGIDA
        3: {"col_name": "posibles_soluciones", "enc_key": "solucion"}
    }
    
    # Mostrar report para cada salida (se necesita el inverse_transform para los nombres de las clases)
    for i, config in target_map.items():
        enc_key = config["enc_key"]
        name = config["col_name"]
        
        # Obtener nombres de las clases reales
        # USANDO EL MAPEO DE CLAVES CORREGIDO: encs[enc_key]
        labels_real = encs[enc_key].inverse_transform(y_test[:, i])
        labels_pred = encs[enc_key].inverse_transform(y_pred[:, i])

        print(f"\n--- Reporte de Clasificación para: {name} ---")
        # El classification_report necesita las etiquetas reales y predichas (numéricas o de string)
        # Aquí usamos las etiquetas string decodificadas para mejor claridad
        print(classification_report(labels_real, labels_pred, zero_division=0))

    print("📌 Guardando modelo en:", MODEL_PATH)
    joblib.dump(modelo, MODEL_PATH)
    print("✅ Entrenamiento finalizado y modelo guardado.")

if __name__ == "__main__":
    entrenar()
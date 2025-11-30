"""
Preprocesamiento: funciones para entrenar transformadores
y para transformar un solo caso en producción.
Guarda los artefactos en app/model/
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder
from scipy.sparse import hstack, csr_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas de artefactos
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
OHE_PATH = os.path.join(BASE_DIR, "ohe.pkl")
ENC_FALLA = os.path.join(BASE_DIR, "enc_falla.pkl")
ENC_SUBFALLA = os.path.join(BASE_DIR, "enc_subfalla.pkl")
ENC_GRAVEDAD = os.path.join(BASE_DIR, "enc_gravedad.pkl")
ENC_SOLUCIONES = os.path.join(BASE_DIR, "enc_soluciones.pkl")
FEATURE_CONFIG = os.path.join(BASE_DIR, "feature_config.pkl")

# Columnas esperadas (según tu especificación)
CAT_COLS = ["marca", "modelo"]
NUM_COLS = [
    "anio", "kilometraje",
    "rpm", "presion_aceite", "temperatura_motor",
    "nivel_combustible", "voltaje_bateria", "velocidad",
    "ultimo_mantenimiento"
]
TEXT_COL = "descripcion_sintomas"

def fit_transform_all(csv_path="dataset.csv", save_artifacts=True):
    """
    Carga dataset.csv, ajusta TF-IDF, OHE, scaler y LabelEncoders.
    Devuelve X (sparse) e y (np.array con 4 columnas).
    Guarda artefactos en app/model/ cuando save_artifacts=True.
    """
    # Intentar cargar el dataset desde la raíz del proyecto
    try:
        df = pd.read_csv(os.path.join(BASE_DIR, "..", "..", csv_path))
    except FileNotFoundError:
        # Fallback si el script se corre desde otra ubicación
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: dataset.csv no encontrado en {os.path.join(BASE_DIR, '..', '..', csv_path)} o directorio actual.")


    # Normalización básica / limpieza
    # fecha -> timestamp days (si existe)
    if "ultimo_mantenimiento" in df.columns:
        df["ultimo_mantenimiento"] = pd.to_datetime(df["ultimo_mantenimiento"], errors="coerce")
        # convertir a días desde hoy (o 0 si NaT)
        ref = pd.Timestamp.now()
        df["ultimo_mantenimiento"] = (ref - df["ultimo_mantenimiento"]).dt.days.fillna(0)

    # Llenar numéricos faltantes con 0 (o mediana si prefieres)
    for c in NUM_COLS:
        if c in df.columns:
            # si columna existe con strings vacíos, convertir a numeric
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # Texto: rellenar vacíos
    df[TEXT_COL] = df.get(TEXT_COL, "").fillna("").astype(str)

    # Targets
    y_falla = df["falla_principal"].astype(str)
    y_subfalla = df["subfalla"].astype(str)
    y_gravedad = df["nivel_gravedad"].astype(str)
    y_soluciones = df["posibles_soluciones"].astype(str)

    # LabelEncoders
    enc_falla = LabelEncoder(); y1 = enc_falla.fit_transform(y_falla)
    enc_sub = LabelEncoder(); y2 = enc_sub.fit_transform(y_subfalla)
    enc_grav = LabelEncoder(); y3 = enc_grav.fit_transform(y_gravedad)
    enc_sol = LabelEncoder(); y4 = enc_sol.fit_transform(y_soluciones)

    # Guardar encoders
    if save_artifacts:
        joblib.dump(enc_falla, ENC_FALLA)
        joblib.dump(enc_sub, ENC_SUBFALLA)
        joblib.dump(enc_grav, ENC_GRAVEDAD)
        joblib.dump(enc_sol, ENC_SOLUCIONES)

    # TF-IDF
    vectorizer = TfidfVectorizer(max_features=1000)
    X_text = vectorizer.fit_transform(df[TEXT_COL].values)

    # OHE para categorias
    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    X_cat = ohe.fit_transform(df[CAT_COLS].fillna(""))

    # Scaler para num
    scaler = MinMaxScaler()
    X_num = scaler.fit_transform(df[NUM_COLS].values)

    # Guardar artefactos
    if save_artifacts:
        joblib.dump(vectorizer, VECTORIZER_PATH)
        joblib.dump(ohe, OHE_PATH)
        joblib.dump(scaler, SCALER_PATH)

    # Concat: num (dense -> sparse), cat (sparse), text (sparse)
    X = hstack([csr_matrix(X_num), X_cat, X_text]).tocsr()
    y = np.column_stack([y1, y2, y3, y4])

    # Guardar feature config (para transformar single input)
    feature_config = {"cat_cols": CAT_COLS, "num_cols": NUM_COLS, "text_col": TEXT_COL}
    if save_artifacts:
        joblib.dump(feature_config, FEATURE_CONFIG)

    return X, y

def transform_single(data: dict):
    """
    Transforma un solo dict (caso) usando artefactos guardados.
    Devuelve X_single (sparse) listo para modelo.predict.
    """
    # Cargar artefactos
    vectorizer = joblib.load(VECTORIZER_PATH)
    ohe = joblib.load(OHE_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_config = joblib.load(FEATURE_CONFIG)

    cat_cols = feature_config["cat_cols"]
    num_cols = feature_config["num_cols"]
    text_col = feature_config["text_col"]

    # Construir DataFrame 1 fila
    df = pd.DataFrame([data])

    # fecha -> días desde ahora
    if "ultimo_mantenimiento" in df.columns:
        df["ultimo_mantenimiento"] = pd.to_datetime(df["ultimo_mantenimiento"], errors="coerce")
        ref = pd.Timestamp.now()
        df["ultimo_mantenimiento"] = (ref - df["ultimo_mantenimiento"]).dt.days.fillna(0)
    else:
        df["ultimo_mantenimiento"] = 0

    # asegurar columnas numéricas
    for c in num_cols:
        if c not in df.columns:
            df[c] = 0
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # asegurar categorías
    for c in cat_cols:
        if c not in df.columns:
            df[c] = ""

    # texto
    if text_col not in df.columns:
        df[text_col] = ""
    
    # Rellenar valores categóricos faltantes para OHE
    for c in cat_cols:
        df[c] = df[c].fillna("")


    # transformar
    X_num = scaler.transform(df[num_cols].values)  # (1, n_num)
    X_cat = ohe.transform(df[cat_cols])
    X_text = vectorizer.transform(df[text_col].values)

    X_single = hstack([csr_matrix(X_num), X_cat, X_text]).tocsr()
    return X_single

# Helpers to load encoders for decoding predictions
def load_label_encoders():
    encs = {
        "falla": joblib.load(ENC_FALLA),
        "subfalla": joblib.load(ENC_SUBFALLA),
        "gravedad": joblib.load(ENC_GRAVEDAD),
        "solucion": joblib.load(ENC_SOLUCIONES)
    }
    return encs
import re
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def limpiar_texto(texto):
    """
    Limpia y normaliza texto descriptivo de fallas.
    """
    if pd.isna(texto):
        return ""
    texto = str(texto).lower()
    texto = re.sub(r"[^a-záéíóúüñ0-9\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def preprocesar_datos(df):
    """
    Recibe un DataFrame con los datos del vehículo y las descripciones.
    Retorna X (características), y (etiquetas) y el preprocessor ajustado.
    """
    df = df.copy()

    # Normalizar columna 'descripcion'
    if "descripcion" in df.columns:
        df["descripcion"] = df["descripcion"].apply(limpiar_texto)
    else:
        df["descripcion"] = ""

    # Columnas esperadas
    columnas_numericas = ["km", "rpm", "presion_aceite", "temperatura_motor"]
    columnas_categoricas = ["marca", "modelo", "anio"]

    # Asegurar existencia de columnas
    for col in columnas_numericas + columnas_categoricas:
        if col not in df.columns:
            df[col] = np.nan

    # Separar etiqueta (si existe)
    y = df["falla"].values if "falla" in df.columns else None

    # Transformadores
    num_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    text_transformer = Pipeline(steps=[
        ("tfidf", TfidfVectorizer(max_features=500))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, columnas_numericas),
            ("cat", cat_transformer, columnas_categoricas),
            ("txt", text_transformer, "descripcion")
        ],
        sparse_threshold=0
    )

    X = preprocessor.fit_transform(df)
    return X, y, preprocessor

def transformar_nuevos_datos(df, preprocessor):
    """
    Aplica un preprocesador ya entrenado.
    """
    df = df.copy()
    if "descripcion" in df.columns:
        df["descripcion"] = df["descripcion"].apply(limpiar_texto)
    else:
        df["descripcion"] = ""
    return preprocessor.transform(df)

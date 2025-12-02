import os
import joblib
import numpy as np

from app.model.preprocess import (
    BASE_DIR,
    load_label_encoders,
    transform_single
)

MODEL_PATH = os.path.join(BASE_DIR, "modelo_multioutput.pkl")


class ModeloServicio:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"No se encontró el modelo entrenado en {MODEL_PATH}")

        self.modelo = joblib.load(MODEL_PATH)
        self.encoders = load_label_encoders()

    def predecir(self, data_dict, umbral_confiabilidad=0.5):

        # Procesar entrada
        X = transform_single(data_dict)  # <<<<<<<<<<<<<<<<<<<<<< USAR ESTA

        # Convertir a 2D si fuera necesario
        if X.ndim == 1:
            X = X.reshape(1, -1)

        pred = self.modelo.predict(X)[0]

        # Decodificar
        nombres = ["falla", "subfalla", "gravedad", "solucion"]
        resultado = {}

        for idx, nombre in enumerate(nombres):
            enc = self.encoders[nombre]
            clase_predicha = enc.inverse_transform([pred[idx]])[0]
            probs = self.modelo.estimators_[idx].predict_proba(X)[0]
            prob_pred = probs[pred[idx]]
            segura = prob_pred >= umbral_confiabilidad
            # decoded = enc.inverse_transform([pred[idx]])[0]
            # resultado[nombre] = decoded
            # Marcar si es incierto
            if prob_pred < umbral_confiabilidad:
                etiqueta_segura = False
            else:
                etiqueta_segura = True
            resultado[nombre] = {
            "prediccion": clase_predicha,
            "confiabilidad": round(float(prob_pred), 4),  # 0.0 a 1.0
            "segura": etiqueta_segura 
            }

        return resultado


def cargar_recursos():
    return ModeloServicio()

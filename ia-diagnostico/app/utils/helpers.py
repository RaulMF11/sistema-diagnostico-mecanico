import re

def limpiar_texto_simple(texto: str) -> str:
    if texto is None:
        return ""
    t = texto.lower()
    t = re.sub(r"[^a-z0-9áéíóúñü\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

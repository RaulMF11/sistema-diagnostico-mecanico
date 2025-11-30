# Imagen base Python
FROM python:3.11-slim

# Setear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Railway maneja PUERTO por variable de entorno
ENV PORT=8000

# Exponer puerto (opcional)
EXPOSE ${PORT}

# Comando para ejecutar usando el puerto dinámico
CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
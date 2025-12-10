# Imagen base Python
FROM python:3.11-slim

# Setear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Exponer puerto de FastAPI
EXPOSE 8000

# Comando para levantar el microservicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
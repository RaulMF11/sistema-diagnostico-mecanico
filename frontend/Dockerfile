# Imagen base de Node
FROM node:20-alpine

# Directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json si existieran
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar todo el proyecto
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Servir con serve (instalarlo)
RUN npm install -g serve

# Exponer puerto 8080
EXPOSE 8080

# Comando por defecto
CMD ["serve", "-s", "dist", "-l", "8080"]

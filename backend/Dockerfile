# Usamos la imagen oficial de PHP con Apache
FROM php:8.2-apache

# Instalar extensiones necesarias
# RUN apt-get update && apt-get install -y unzip git curl \
#     && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
#     && docker-php-ext-install pdo pdo_mysql
RUN apt-get update && apt-get install -y \
        libpq-dev \
        unzip \
        git \
        curl \
    && docker-php-ext-install pdo pdo_pgsql pgsql \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Copiar código al contenedor
WORKDIR /var/www/html
COPY . .

# Instalar dependencias de Composer
RUN composer install --no-dev --optimize-autoloader

# Habilitar mod_rewrite de Apache
RUN a2enmod rewrite

# Exponer puerto 8000
EXPOSE 8000

# Comando por defecto
CMD ["php", "-S", "0.0.0.0:8000", "-t", "public"]

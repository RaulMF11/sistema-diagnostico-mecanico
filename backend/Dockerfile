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
        libzip-dev \
        libonig-dev \
    && docker-php-ext-install pdo pdo_pgsql pgsql mbstring zip \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Copiar código al contenedor
WORKDIR /var/www/html
COPY . .

# Instalar dependencias de Composer
RUN composer install --no-dev --optimize-autoloader

# Habilitar mod_rewrite de Apache
RUN a2enmod rewrite

# Dar permisos a storage y bootstrap/cache
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache \
    && chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

# Exponer puerto 8000
EXPOSE 80

# Comando por defecto
CMD ["apache2-foreground"]

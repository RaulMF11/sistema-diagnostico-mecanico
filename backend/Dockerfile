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
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar código Laravel al contenedor
WORKDIR /var/www/html
COPY . .

# Instalar dependencias de Composer
RUN composer install --no-dev --optimize-autoloader

# Habilitar mod_rewrite de Apache
RUN a2enmod rewrite

# Ajustar DocumentRoot para servir /public
RUN sed -i 's|DocumentRoot /var/www/html|DocumentRoot /var/www/html/public|g' /etc/apache2/sites-available/000-default.conf

# Dar permisos correctos a storage y bootstrap/cache
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache \
    && chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

# Establecer puerto 80 (Apache)
EXPOSE 80

# Comando final: ejecutar migraciones y levantar Apache
CMD php artisan migrate --force && apache2-foreground

# Etapa 1: Build - Instalar dependencias
FROM python:3.12-slim as builder

WORKDIR /app

# Instalar dependencias de build
RUN pip install --upgrade pip

# Copiar fichero de dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 2: Final - Configurar la imagen de producción
FROM python:3.12-slim

# Crear un usuario no-root para ejecutar la aplicación
RUN addgroup --system app && adduser --system --group app

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas de la etapa de build
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copiar el código de la aplicación
COPY . .

# Cambiar el propietario de los ficheros al usuario no-root
RUN chown -R app:app /app

# Cambiar al usuario no-root
USER app

# Exponer el puerto en el que corre la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
# --host 0.0.0.0 es necesario para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

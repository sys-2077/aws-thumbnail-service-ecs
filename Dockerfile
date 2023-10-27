# Utilizamos una imagen base con Python
FROM python:3.8

# Instalamos las bibliotecas necesarias
RUN pip install boto3 pillow

# Copiamos el script de Python y el archivo de configuración (si es necesario) al contenedor
COPY transform_image.py /app/
# COPY config.json /app/ (si es necesario)

# Establecemos el directorio de trabajo
WORKDIR /app

# Comando para ejecutar el script de transformación
CMD ["python", "transform_image.py"]

import os
import sys
import boto3
from PIL import Image

# Configuración de AWS
aws_access_key_id = ''
aws_secret_access_key = ''
region_name = 'us-east-2'

# Nombres de los buckets
input_bucket_name = 'input-images-1'
output_bucket_name = 'output-thumbnail-1'

# Inicializamos el cliente de S3
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# Obtenemos la lista de objetos en el bucket de entrada
objects = s3.list_objects(Bucket=input_bucket_name)
if 'Contents' in objects:
    for obj in objects['Contents']:
        input_image_key = obj['Key']

        # Descargamos la imagen del bucket de entrada
        s3.download_file(input_bucket_name, input_image_key, input_image_key)

        # Abrimos la imagen y la transformamos
        try:
            with Image.open(input_image_key) as img:
                img.thumbnail((100, 100))
                img.save("thumbnail_" + input_image_key)

            # Subimos la miniatura al bucket de salida
            s3.upload_file("thumbnail_" + input_image_key, output_bucket_name, "thumbnail_" + input_image_key)

            # Movemos la imagen original a la carpeta "processed" en el bucket de entrada
            s3.copy_object(Bucket=input_bucket_name, CopySource=input_bucket_name + '/' + input_image_key, Key='processed/' + input_image_key)
            s3.delete_object(Bucket=input_bucket_name, Key=input_image_key)

        except Exception as e:
            print(f"Error processing {input_image_key}: {e}")
        finally:
            # Eliminamos los archivos locales
            os.remove(input_image_key)
            os.remove("thumbnail_" + input_image_key)
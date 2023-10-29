import os
import sys
import boto3
from PIL import Image

def main():
    # Recover AWS credentials from environmental variables
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    # Bucket names
    input_bucket_name = os.environ.get("INPUT_BUCKET_NAME")
    output_bucket_name = os.environ.get("OUTPUT_BUCKET_NAME")
    # Region name
    region_name = os.environ.get("REGION_NAME")

    if not (aws_access_key_id and aws_secret_access_key):
        print("No AWS credentials were provided. Be sure to configure environment variables...")
        return

    # Create a S3 client
    s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    

    # Initialize S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    # We get the list of objects in the entrance bucket
    objects = s3.list_objects(Bucket=input_bucket_name)
    if 'Contents' in objects:
        for obj in objects['Contents']:
            input_image_key = obj['Key']

            # Download the entry bucket image
            s3.download_file(input_bucket_name, input_image_key, input_image_key)

            # Open the image and transform it
            try:
                with Image.open(input_image_key) as img:
                    img.thumbnail((100, 100))
                    img.save("thumbnail_" + input_image_key)

                # We upload the miniature to the output bucket
                s3.upload_file("thumbnail_" + input_image_key, output_bucket_name, "thumbnail_" + input_image_key)

                # Move the original image to the "Processsed" folder in the entrance bucket
                s3.copy_object(Bucket=input_bucket_name, CopySource=input_bucket_name + '/' + input_image_key, Key='processed/' + input_image_key)
                s3.delete_object(Bucket=input_bucket_name, Key=input_image_key)

            except Exception as e:
                print(f"Error processing {input_image_key}: {e}")
            finally:
                # Drop local files
                os.remove(input_image_key)
                os.remove("thumbnail_" + input_image_key)

if __name__ == "__main__":
    main()
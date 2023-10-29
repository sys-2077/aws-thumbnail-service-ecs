# Use a base image with python
FROM python:3.8
# Install the necessary libraries
#RUN pip install boto3 pillow
# Copy the Python script and the configuration file to the container
COPY ./app/transform_image.py /app/
# Establish the work board
WORKDIR /app

# Set the environment variables
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG INPUT_BUCKET_NAME
ARG OUTPUT_BUCKET_NAME
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV INPUT_BUCKET_NAME=$INPUT_BUCKET_NAME
ENV OUTPUT_BUCKET_NAME=$OUTPUT_BUCKET_NAME


# Excute the Python script
CMD ["python", "transform_image.py"]

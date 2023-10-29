# Use a base image with python
FROM python:3.8
# Install the necessary libraries
RUN pip install boto3 pillow
# Copy the Python script and the configuration file to the container
COPY transform_image.py /app/
# Establish the work board
WORKDIR /app
# Excute the Python script
CMD ["python", "transform_image.py"]

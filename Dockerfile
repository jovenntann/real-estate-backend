# Use Python 3.12 as the base image
FROM python:3.12

# We are using the docker-compose-wait tool in this Dockerfile
# This tool is used to control the startup order of services in Docker Compose
# For more details about this tool, visit the following link:
# https://github.com/ufoscout/docker-compose-wait

# Add the wait script to the image from the specified URL
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait

# Change the permissions of the wait script to make it executable
RUN chmod +x /wait

# Set the PYTHONUNBUFFERED environment variable to 1
# This ensures that Python output is sent straight to terminal without being first buffered
ENV PYTHONUNBUFFERED=1

# Set the working directory in the Docker image to /app
WORKDIR /app

# Copy the requirements.txt file from your host to the present location (/app/) in the Docker image
COPY requirements.txt /app/

# Install the Python dependencies specified in the requirements.txt file
RUN pip install -r requirements.txt

# Copy the rest of your host's current directory contents into the Docker image
COPY . /app/
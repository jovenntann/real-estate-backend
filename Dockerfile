
# Use Python 3.12 as the base image
FROM python:3.12

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

# Expose port 8000 for the application
# This is the port your Django app will be running on
EXPOSE 8000

# Command to run the Django server
# This command will first make migrations without any user input
# Then it will migrate the database, again without any user input
# Finally, it will start the Gunicorn server and bind it to the exposed port
CMD sh -c "\
    python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    gunicorn tappy.wsgi:application --bind 0.0.0.0:8000"

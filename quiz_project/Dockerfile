FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set environment variables for Django settings
ENV PYTHONUNBUFFERED 1

# Expose the port Django will run on
EXPOSE 8000

# Run the Django server (you can use gunicorn or manage.py for production)
CMD ["python", "manage.py", "runserver"]

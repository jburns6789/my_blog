# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

#Install dependencies 
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose the application port
EXPOSE 8000

# Collect static files and run migrations during the build
RUN python manage.py collectstatic --noinput

# Start the application
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000","--workers", "3"]

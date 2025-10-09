# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies 
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=production

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Create entrypoint script, enable during production
#COPY docker-entrypoint.prod.sh /docker-entrypoint.sh
#RUN chmod +x /docker-entrypoint.sh

# Expose the application port
EXPOSE 8000

# Use entrypoint script, enable during production
#ENTRYPOINT ["/docker-entrypoint.sh"]

# Start the application
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

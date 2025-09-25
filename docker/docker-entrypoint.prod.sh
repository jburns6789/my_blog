#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database..."
until python manage.py shell -c "
import django
django.setup()
from django.db import connection
connection.ensure_connection()
print('Database is ready!')
"; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Database is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (optional)
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found. Please create one manually.')
"

# Execute the main command
echo "Starting application..."
exec "$@"

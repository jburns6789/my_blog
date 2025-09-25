"""
Settings package initialization
"""
import os

# Default to local settings if no environment is specified
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'local')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'local':
    from .development import *
else:
    from .development import *

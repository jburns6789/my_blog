"""
Local production testing settings
"""
from .base import *

env.read_env(BASE_DIR / '.env.local-prod')

# Production-like settings but safe for local testing
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Use PostgreSQL locally (via Docker)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('DATABASE_HOST', default='localhost'),
        'PORT': env('DATABASE_PORT', default='5433'),
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email backend for testing (console instead of SMTP)
if env('EMAIL_BACKEND', default='console') == 'console':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='djangotesting8@gmail.com')
    CONTACT_EMAIL = env('CONTACT_EMAIL', default=DEFAULT_FROM_EMAIL)

# Production security settings (but relaxed for local testing)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Don't enforce HTTPS locally
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

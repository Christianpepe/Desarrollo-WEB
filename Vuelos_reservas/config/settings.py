
import os
from pathlib import Path
# from dotenv import load_dotenv  # Eliminado para producción
from decouple import config
# Para Railway: importar dj-database-url
import dj_database_url
#CORONA GARCIA CHRISTIAN JAVIER

# Configuración de correo SMTP para Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

HCAPTCHA_SITE_KEY = os.getenv('HCAPTCHA_SITE_KEY')
HCAPTCHA_SECRET_KEY = os.getenv('HCAPTCHA_SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "clave_de_prueba")

DEBUG = True
ALLOWED_HOSTS = ['desarrollo-web-production.up.railway.app', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tus apps
    'apps.usuarios',
   
    'apps.reservas',
    'apps.notificaciones',
    'apps.vuelos.apps.VuelosConfig',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Usa tu carpeta de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

AUTH_USER_MODEL = 'usuarios.Usuario'

# Configuración de autenticación
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
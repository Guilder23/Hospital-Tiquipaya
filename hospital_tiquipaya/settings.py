import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-change-me')
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes', 'on')

ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if host.strip()]
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()]
INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'apps.pacientes','apps.especialidades','apps.horarios','apps.citas','apps.accounts','apps.ecografias',
    'apps.contratos','apps.citas_ecografia','apps.permisos','apps.dashboard'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'apps.permisos.middleware.PermisosMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]
ROOT_URLCONF = 'hospital_tiquipaya.urls'
TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[BASE_DIR/'templates'],
    'APP_DIRS':True,
    'OPTIONS':{'context_processors':[
        'django.template.context_processors.debug','django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages',
        'apps.citas.context_processors.paciente',
        'apps.permisos.context_processors.permisos_usuario'
    ]}
}]
WSGI_APPLICATION = 'hospital_tiquipaya.wsgi.application'
DATABASES = {'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

MESSAGE_TAGS = {
    'debug': 'info',
    'info': 'info',
    'success': 'success',
    'warning': 'warning',
    'error': 'error',
}

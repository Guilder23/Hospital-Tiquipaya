import os
import sys
from pathlib import Path

PROJECT_DIR = Path('/home/TU_USUARIO/Hospital-Tiquipaya-Oficial')
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
os.environ.setdefault('DJANGO_DEBUG', 'False')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', 'TU_USUARIO.pythonanywhere.com')
os.environ.setdefault('DJANGO_CSRF_TRUSTED_ORIGINS', 'https://TU_USUARIO.pythonanywhere.com')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

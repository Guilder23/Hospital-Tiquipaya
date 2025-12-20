import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from apps.permisos.models import Modulo

modulos = Modulo.objects.all().order_by('nombre')
print(f"\n{'ID':<3} {'NOMBRE':<40} {'URL':<40} {'ACTIVO':<7}")
print("=" * 90)
for m in modulos:
    print(f"{m.id:<3} {m.nombre:<40} {m.url:<40} {str(m.activo):<7}")

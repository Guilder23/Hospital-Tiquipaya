import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from apps.accounts.models import TipoUsuario
from apps.permisos.models import Permiso

# Obtener tipo Médico
tipo_medico = TipoUsuario.objects.filter(nombre='Medico').first()
tipo_ecografo = TipoUsuario.objects.filter(nombre='Ecografo').first()

if tipo_medico:
    print(f"\n=== MÉDICO ===")
    permisos = Permiso.objects.filter(tipo_usuario=tipo_medico).select_related('modulo')
    print(f"{'Modulo':<40} {'Visible':<7} {'Tipo Permiso':<15}")
    print("=" * 62)
    for p in permisos:
        print(f"{p.modulo.nombre:<40} {str(p.visible):<7} {p.tipo_permiso:<15}")

if tipo_ecografo:
    print(f"\n=== ECÓGRAFO ===")
    permisos = Permiso.objects.filter(tipo_usuario=tipo_ecografo).select_related('modulo')
    print(f"{'Modulo':<40} {'Visible':<7} {'Tipo Permiso':<15}")
    print("=" * 62)
    for p in permisos:
        print(f"{p.modulo.nombre:<40} {str(p.visible):<7} {p.tipo_permiso:<15}")

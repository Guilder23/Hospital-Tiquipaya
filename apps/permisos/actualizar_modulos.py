"""
Script para marcar módulos como no asignables
Ejecutar con: Get-Content apps/permisos/actualizar_modulos.py | python manage.py shell
"""

from apps.permisos.models import Modulo

print("=" * 60)
print("ACTUALIZANDO MÓDULOS - MARCAR COMO NO ASIGNABLES")
print("=" * 60)

# Módulos que NO deben aparecer en la gestión de permisos
modulos_no_asignables = [
    'Mis Citas Médicas',
    'Pacientes Atendidos',
    'Mis Citas Ecografía',
    'Pacientes Ecografía',
]

for nombre in modulos_no_asignables:
    try:
        modulo = Modulo.objects.get(nombre=nombre)
        modulo.asignable = False
        modulo.save()
        print(f"✓ {nombre} → No asignable")
    except Modulo.DoesNotExist:
        print(f"⚠ Módulo no encontrado: {nombre}")

print("\n" + "=" * 60)
print("PROCESO COMPLETADO")
print("=" * 60)

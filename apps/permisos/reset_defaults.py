"""
Resetear módulos por defecto y permisos para Medico y Ecografo
Ejecutar con: Get-Content apps/permisos/reset_defaults.py | python manage.py shell
"""
from apps.permisos.models import Modulo, Permiso
from apps.accounts.models import TipoUsuario

roles = {
    'Medico': ['Dashboard', 'Mis Citas Médicas', 'Pacientes Atendidos'],
    'Ecografo': ['Dashboard', 'Mis Citas Ecografía', 'Pacientes Ecografía'],
}

print('='*60)
print('RESETEANDO MÓDULOS POR DEFECTO Y PERMISOS')
print('='*60)

# Build modulo cache
mods = {m.nombre: m for m in Modulo.objects.all()}

for role_name, default_names in roles.items():
    try:
        tipo = TipoUsuario.objects.get(nombre=role_name)
    except TipoUsuario.DoesNotExist:
        print(f"⚠ TipoUsuario no encontrado: {role_name}")
        continue

    # Reset defaults
    tipo.modulos_por_defecto.clear()
    for name in default_names:
        mod = mods.get(name)
        if mod:
            tipo.modulos_por_defecto.add(mod)
            print(f"✓ {role_name}: por defecto → {name}")
        else:
            print(f"⚠ Módulo no existe: {name}")

    allowed = set(default_names) | {'Dashboard'}

    # Reset permisos: everything not allowed → sin acceso
    for m in Modulo.objects.all():
        if m.nombre not in allowed:
            Permiso.objects.update_or_create(
                tipo_usuario=tipo,
                modulo=m,
                defaults={'visible': False, 'tipo_permiso': 'sin_acceso'}
            )
    print(f"✓ {role_name}: permisos restantes en sin acceso")

print('\n' + '='*60)
print('PROCESO COMPLETADO')
print('='*60)

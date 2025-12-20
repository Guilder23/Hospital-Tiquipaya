"""
Script para poblar módulos y permisos iniciales del sistema
Ejecutar con: Get-Content apps/permisos/poblar_datos.py | python manage.py shell
"""

from apps.permisos.models import Modulo, Permiso
from apps.accounts.models import TipoUsuario

print("=" * 60)
print("POBLANDO MÓDULOS Y PERMISOS INICIALES")
print("=" * 60)

# Crear módulos del sistema
modulos_data = [
    {'nombre': 'Dashboard', 'url': '/home/', 'icono': 'fas fa-home', 'orden': 1},
    {'nombre': 'Pacientes', 'url': '/pacientes/', 'icono': 'fas fa-users', 'orden': 2},
    {'nombre': 'Citas Médicas', 'url': '/citas/', 'icono': 'fas fa-calendar-alt', 'orden': 3},
    {'nombre': 'Mis Citas Médicas', 'url': '/citas/medico/hoy/', 'icono': 'fas fa-calendar-check', 'orden': 3.5},
    {'nombre': 'Pacientes Atendidos', 'url': '/citas/medico/atendidos/', 'icono': 'fas fa-user-check', 'orden': 3.7},
    {'nombre': 'Ecografías', 'url': '/ecografias/', 'icono': 'fas fa-image', 'orden': 4},
    {'nombre': 'Citas Ecografía', 'url': '/citas-ecografia/', 'icono': 'fas fa-stethoscope', 'orden': 5},
    {'nombre': 'Mis Citas Ecografía', 'url': '/citas-ecografia/mis-citas/', 'icono': 'fas fa-calendar-check', 'orden': 5.5},
    {'nombre': 'Pacientes Ecografía', 'url': '/citas-ecografia/pacientes-atendidos/', 'icono': 'fas fa-user-check', 'orden': 5.7},
    {'nombre': 'Especialidades', 'url': '/especialidades/', 'icono': 'fas fa-user-md', 'orden': 6},
    {'nombre': 'Turnos', 'url': '/turnos/', 'icono': 'fas fa-clock', 'orden': 7},
    {'nombre': 'Contratos', 'url': '/contratos/', 'icono': 'fas fa-file-contract', 'orden': 8},
    {'nombre': 'Usuarios', 'url': '/usuarios/', 'icono': 'fas fa-user', 'orden': 9},
    {'nombre': 'Tipos de Usuario', 'url': '/tipos/', 'icono': 'fas fa-user-tag', 'orden': 10},
    {'nombre': 'Gestión de Permisos', 'url': '/permisos/', 'icono': 'fas fa-shield-alt', 'orden': 11},
]

modulos = {}
for data in modulos_data:
    modulo, created = Modulo.objects.get_or_create(
        nombre=data['nombre'],
        defaults={
            'url': data['url'],
            'icono': data['icono'],
            'orden': data['orden']
        }
    )
    modulos[data['nombre']] = modulo
    if created:
        print(f"  ✓ Módulo creado: {data['nombre']}")
    else:
        print(f"  → Módulo existente: {data['nombre']}")

print(f"\nMódulos en total: {Modulo.objects.count()}")

# Asignar módulos por defecto a roles
print("\n" + "=" * 60)
print("ASIGNANDO MÓDULOS POR DEFECTO A ROLES")
print("=" * 60)

modulos_por_defecto = {
    # Solo 3 por defecto para Medico y Ecografo
    'Medico': ['Dashboard', 'Mis Citas Médicas', 'Pacientes Atendidos'],
    'Ecografo': ['Dashboard', 'Mis Citas Ecografía', 'Pacientes Ecografía'],
}

tipos = TipoUsuario.objects.all()
for tipo in tipos:
    tipo_nombre_lower = tipo.nombre.lower().strip()
    
    for key, modulo_nombres in modulos_por_defecto.items():
        if key.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') == tipo_nombre_lower.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u'):
            print(f"\n📋 {tipo.nombre}:")
            # Limpiar módulos por defecto anteriores
            tipo.modulos_por_defecto.clear()
            for modulo_nombre in modulo_nombres:
                if modulo_nombre in modulos:
                    tipo.modulos_por_defecto.add(modulos[modulo_nombre])
                    print(f"  ✓ Agregado por defecto: {modulo_nombre}")

# Configurar permisos por tipo de usuario
print("\n" + "=" * 60)
print("CONFIGURANDO PERMISOS POR TIPO DE USUARIO")
print("=" * 60)

if not tipos.exists():
    print("⚠ No hay tipos de usuario creados. Primero crea tipos de usuario.")
else:
    print(f"\nTipos de usuario encontrados: {tipos.count()}")
    
    # Configuración de permisos por tipo
    permisos_config = {
        'Administrador': {
            'todos': 'editor'  # Administrador tiene acceso completo a todo
        },
        # Por defecto, médico y ecógrafo no tendrán permisos adicionales
        # (solo verán sus 3 módulos por defecto hasta que el admin asigne más)
        'Medico': {
            'Dashboard': 'solo_vista',
        },
        'Ecografo': {
            'Dashboard': 'solo_vista',
        },
    }
    
    permisos_count = 0
    
    for tipo in tipos:
        print(f"\n📋 Configurando: {tipo.nombre}")
        
        # Buscar configuración con case-insensitive
        config = None
        tipo_nombre_lower = tipo.nombre.lower().strip()
        
        for key in permisos_config.keys():
            if key.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') == tipo_nombre_lower.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u'):
                config = permisos_config[key]
                break
        
        if config:
            
            # Si tiene acceso a "todos", dar acceso completo
            if 'todos' in config:
                tipo_permiso = config['todos']
                for modulo in Modulo.objects.all():
                    permiso, created = Permiso.objects.update_or_create(
                        tipo_usuario=tipo,
                        modulo=modulo,
                        defaults={
                            'visible': True,
                            'tipo_permiso': tipo_permiso
                        }
                    )
                    permisos_count += 1
                    print(f"  ✓ {modulo.nombre}: {tipo_permiso}")
            else:
                # Configurar permisos específicos
                for modulo_nombre, tipo_permiso in config.items():
                    if modulo_nombre in modulos:
                        modulo = modulos[modulo_nombre]
                        permiso, created = Permiso.objects.update_or_create(
                            tipo_usuario=tipo,
                            modulo=modulo,
                            defaults={
                                'visible': True,
                                'tipo_permiso': tipo_permiso
                            }
                        )
                        permisos_count += 1
                        print(f"  ✓ {modulo.nombre}: {tipo_permiso}")

                # Poner el resto de módulos en sin acceso (no visibles) para este tipo
                # Permitidos: los del config y los por defecto
                # Encontrar clave original coincidente
                matched_key = None
                for key in modulos_por_defecto.keys():
                    if key.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') == tipo_nombre_lower.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u'):
                        matched_key = key
                        break
                default_names = set(modulos_por_defecto.get(matched_key, []))
                allowed_names = set(config.keys()) | default_names
                for modulo in Modulo.objects.all():
                    if modulo.nombre not in allowed_names:
                        Permiso.objects.update_or_create(
                            tipo_usuario=tipo,
                            modulo=modulo,
                            defaults={'visible': False, 'tipo_permiso': 'sin_acceso'}
                        )
        else:
            print(f"  ⚠ Sin configuración predefinida")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"Módulos creados: {Modulo.objects.count()}")
print(f"Permisos configurados: {permisos_count}")
print(f"Tipos de usuario: {tipos.count()}")
print("=" * 60)
print("✓ PROCESO COMPLETADO")
print("=" * 60)
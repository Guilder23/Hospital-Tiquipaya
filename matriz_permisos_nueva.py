"""
Script para verificar el comportamiento completo de permisos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from django.contrib.auth.models import User
from apps.accounts.models import Perfil, TipoUsuario
from apps.permisos.models import Modulo, Permiso
from apps.permisos.utils import es_admin_o_staff, PermisoAdmin

print("=" * 100)
print("MATRIZ COMPLETA DE COMPORTAMIENTO DE PERMISOS")
print("=" * 100)

tipos_usuarios = [
    ('Encargado de Admision', 'editor'),
    ('Recepcion de Admision', 'solo_vista'),
    ('Medico', 'solo_vista'),
]

modulo_test = Modulo.objects.filter(nombre__icontains="Especialidad").first()

for tipo_nombre, permiso_esperado in tipos_usuarios:
    tipo = TipoUsuario.objects.filter(nombre=tipo_nombre).first()
    
    if tipo:
        print(f"\n{'─' * 100}")
        print(f"👤 TIPO: {tipo_nombre}")
        print(f"{'─' * 100}")
        
        usuarios = User.objects.filter(perfil__tipo=tipo).first()
        
        if usuarios:
            usuario = usuarios
            
            print(f"Usuario: {usuario.username}")
            print(f"is_staff: {usuario.is_staff}")
            print(f"es_admin_o_staff(): {es_admin_o_staff(usuario)}")
            
            # Obtener permiso
            try:
                permiso = Permiso.objects.get(
                    tipo_usuario=tipo,
                    modulo=modulo_test
                )
                
                print(f"\nPermiso en '{modulo_test.nombre}':")
                print(f"├─ visible: {permiso.visible}")
                print(f"├─ tipo_permiso: {permiso.tipo_permiso}")
                print(f"├─ puede_editar(): {permiso.puede_editar()}")
                print(f"└─ es_solo_vista(): {permiso.es_solo_vista()}")
                
                # Determinar qué ve el usuario
                print(f"\n📺 QUÉ VE EL USUARIO:")
                if not permiso.visible:
                    print(f"   ❌ No aparece el módulo en sidebar")
                else:
                    print(f"   ✅ Módulo aparece en sidebar")
                    print(f"   ✅ Puede ver los datos")
                    
                    if permiso.puede_editar():
                        print(f"   ✅ VE botones: Crear, Editar, Desactivar")
                        print(f"   ✅ PUEDE: crear, editar, eliminar")
                    else:
                        print(f"   ❌ NO VE botones de CRUD")
                        print(f"   ✅ SOLO puede: ver")
                        
            except Permiso.DoesNotExist:
                print(f"❌ No hay permiso asignado para este módulo")

# Verificar admin
print(f"\n{'─' * 100}")
print(f"👤 TIPO: ADMINISTRADOR (Superusuario)")
print(f"{'─' * 100}")

admin = User.objects.filter(is_superuser=True).first()
if admin:
    print(f"Usuario: {admin.username}")
    print(f"is_superuser: {admin.is_superuser}")
    print(f"es_admin_o_staff(): {es_admin_o_staff(admin)}")
    
    print(f"\n✅ ACCESO:")
    print(f"   ✅ VE TODOS los módulos")
    print(f"   ✅ Puede crear, editar, eliminar EN TODO")

print(f"\n{'=' * 100}")
print("✨ FIN DE MATRIZ")
print("=" * 100)

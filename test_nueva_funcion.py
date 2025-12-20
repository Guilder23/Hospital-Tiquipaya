"""
Script para simular una petición y verificar los permisos con la nueva función
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
print("SIMULACIÓN DE PETICIÓN HTTP CON NUEVA FUNCIÓN")
print("=" * 100)

# Obtener el tipo de usuario "Encargado de Admisión"
tipo_encargado = TipoUsuario.objects.filter(nombre__icontains="Encargado").first()

usuarios_test = User.objects.filter(perfil__tipo=tipo_encargado).values_list('username', flat=True)[:1]

if usuarios_test:
    usuario = User.objects.get(username=usuarios_test[0])
    print(f"\n✅ Usuario de prueba: {usuario.username}")
    
    print(f"\n📝 Detalles del usuario:")
    print(f"   - Username: {usuario.username}")
    print(f"   - is_superuser: {usuario.is_superuser}")
    print(f"   - is_staff: {usuario.is_staff}")
    print(f"   - Tipo de usuario: {usuario.perfil.tipo}")
    
    print(f"\n🔍 Validación con la NUEVA función:")
    print(f"   - es_admin_o_staff({usuario.username}): {es_admin_o_staff(usuario)}")
    
    # Obtener módulo de Especialidades
    modulo = Modulo.objects.filter(nombre__icontains="Especialidad").first()
    
    if modulo:
        print(f"\n📌 Verificando acceso a: {modulo.nombre}")
        
        # Obtener el permiso
        try:
            permiso = Permiso.objects.get(
                tipo_usuario=usuario.perfil.tipo,
                modulo=modulo
            )
            
            print(f"\n   ✅ Permiso encontrado:")
            print(f"      - visible: {permiso.visible}")
            print(f"      - tipo_permiso: {permiso.tipo_permiso}")
            print(f"      - puede_editar(): {permiso.puede_editar()}")
            
            print(f"\n🎯 RESULTADO EN LA APLICACIÓN:")
            if permiso.puede_editar():
                print(f"   ✅ Usuario puede crear, editar, eliminar en esta sección")
            else:
                print(f"   👁️ Usuario solo puede ver en esta sección")
                
        except Permiso.DoesNotExist:
            print(f"   ❌ No hay permiso asignado")

# Verificar también el administrador
print(f"\n" + "=" * 100)
print("VERIFICACIÓN: ADMINISTRADOR")
print("=" * 100)

admin = User.objects.filter(is_superuser=True).first()
if admin:
    print(f"\n✅ Usuario admin: {admin.username}")
    print(f"   - is_superuser: {admin.is_superuser}")
    print(f"   - es_admin_o_staff(): {es_admin_o_staff(admin)}")
    print(f"   - Resultado: ✅ ACCESO TOTAL (PermisoAdmin)")

print("\n" + "=" * 100)

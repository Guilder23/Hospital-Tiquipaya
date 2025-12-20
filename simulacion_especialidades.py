"""
Diagnóstico: Simular exactamente lo que pasa cuando 
un usuario con permiso 'editor' intenta ver /especialidades/
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from django.contrib.auth.models import User
from apps.accounts.models import Perfil
from apps.permisos.models import Permiso, Modulo
from apps.permisos.utils import es_admin_o_staff, PermisoAdmin

print("=" * 100)
print("SIMULACIÓN: ¿Qué pasa cuando Encargado va a /especialidades/?")
print("=" * 100)

# Obtener usuario encargado
usuario = User.objects.filter(username='encargado').first()

if usuario:
    print(f"\n👤 Usuario: {usuario.username}")
    print(f"   is_staff: {usuario.is_staff}")
    print(f"   is_superuser: {usuario.is_superuser}")
    
    # Validación 1: Middleware
    print(f"\n1️⃣ MIDDLEWARE VALIDA:")
    print(f"   - es_admin_o_staff({usuario.username})? {es_admin_o_staff(usuario)}")
    
    if not es_admin_o_staff(usuario):
        print(f"   → No es admin, obtiene permisos específicos")
        
        # Buscar módulo de especialidades
        modulo = Modulo.objects.filter(nombre__icontains="Especialidad").first()
        
        if modulo:
            print(f"\n2️⃣ BUSCA MÓDULO POR URL:")
            print(f"   - URL: /especialidades/")
            print(f"   - Módulo encontrado: {modulo.nombre}")
            
            # Obtener permiso
            try:
                permiso = Permiso.objects.get(
                    tipo_usuario=usuario.perfil.tipo,
                    modulo=modulo
                )
                
                print(f"\n3️⃣ PERMISO ENCONTRADO EN BD:")
                print(f"   - visible: {permiso.visible}")
                print(f"   - tipo_permiso: {permiso.tipo_permiso}")
                print(f"   - tiene_acceso(): {permiso.tiene_acceso()}")
                print(f"   - puede_editar(): {permiso.puede_editar()}")
                
                print(f"\n4️⃣ ASIGNA A REQUEST:")
                print(f"   - request.permiso_actual = {permiso}")
                
                print(f"\n5️⃣ EN LA VISTA:")
                print(f"   - Pasa al template: permiso_actual = {permiso}")
                
                print(f"\n6️⃣ EN EL TEMPLATE (specialties.html):")
                print(f"   - {{% if user.is_superuser or permiso_actual.puede_editar %}}")
                
                # Simulación del template
                condicion = usuario.is_superuser or permiso.puede_editar()
                print(f"   - user.is_superuser = {usuario.is_superuser}")
                print(f"   - OR permiso_actual.puede_editar() = {permiso.puede_editar()}")
                print(f"   - Resultado: {usuario.is_superuser} OR {permiso.puede_editar()} = {condicion}")
                
                if condicion:
                    print(f"\n   ✅ MUESTRA BOTONES:")
                    print(f"      • Nueva Especialidad")
                    print(f"      • Editar")
                    print(f"      • Desactivar")
                else:
                    print(f"\n   ❌ NO MUESTRA BOTONES")
                    print(f"      (Solo muestra botón 'Ver')")
                
            except Permiso.DoesNotExist:
                print(f"   ❌ PERMISO NO ENCONTRADO!")
                print(f"   → Usuario NO tiene acceso")
    else:
        print(f"   → Es admin, obtiene PermisoAdmin (acceso total)")

print("\n" + "=" * 100)

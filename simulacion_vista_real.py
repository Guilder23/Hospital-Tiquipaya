#!/usr/bin/env python
"""
Simulación completa de lo que ocurre cuando un usuario accede a /especialidades/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from django.contrib.auth.models import User
from apps.accounts.models import Perfil
from apps.permisos.models import Permiso, Modulo
from apps.especialidades.views import lista_especialidades
from django.test import RequestFactory
from apps.permisos.middleware import PermisosMiddleware
from apps.permisos.utils import es_admin_o_staff

print("=" * 120)
print("SIMULACIÓN: USUARIO ENCARGADO ACCEDIENDO A /especialidades/")
print("=" * 120)

# 1. Obtener usuario encargado
usuario = User.objects.filter(username='encargado').first()
if not usuario:
    print("❌ Usuario 'encargado' no encontrado")
    exit(1)

print(f"\n👤 Usuario: {usuario.username}")
print(f"   - is_staff: {usuario.is_staff}")
print(f"   - is_superuser: {usuario.is_superuser}")
print(f"   - perfil.tipo: {usuario.perfil.tipo.nombre}")

# 2. Crear mock request
factory = RequestFactory()
request = factory.get('/especialidades/')
request.user = usuario

print(f"\n🌐 Request a: {request.path}")

# 3. Aplicar middleware (simular lo que hace el middleware)
print("\n🔄 PROCESAMIENTO POR MIDDLEWARE:")
print("-" * 120)

# Paso 1: Verificar si es admin/staff
es_admin = es_admin_o_staff(usuario)
print(f"   ¿es_admin_o_staff(usuario)? {es_admin}")

if es_admin:
    print("   ➜ Es admin/staff → Asignar PermisoAdmin (acceso total)")
else:
    print("   ➜ NO es admin/staff → Buscar permisos específicos")
    
    # Paso 2: Obtener tipo de usuario
    tipo_usuario = usuario.perfil.tipo
    print(f"\n   Tipo de usuario: {tipo_usuario.nombre}")
    
    # Paso 3: Obtener módulo por URL
    middleware = PermisosMiddleware(lambda r: None)
    modulo = middleware.obtener_modulo_por_url(request.path)
    
    if modulo:
        print(f"   Módulo encontrado: {modulo.nombre}")
        
        # Paso 4: Buscar permiso
        try:
            permiso = Permiso.objects.get(tipo_usuario=tipo_usuario, modulo=modulo)
            
            print(f"\n   ✅ PERMISO ENCONTRADO:")
            print(f"      - tipo_permiso: {permiso.tipo_permiso}")
            print(f"      - visible: {permiso.visible}")
            print(f"      - tiene_acceso(): {permiso.tiene_acceso()}")
            print(f"      - es_solo_vista(): {permiso.es_solo_vista()}")
            print(f"      - puede_editar(): {permiso.puede_editar()}")
            
            # Paso 5: Verificar condición en template
            print("\n   Template usa: {% if user.is_superuser or permiso_actual.puede_editar %}")
            
            condicion = usuario.is_superuser or permiso.puede_editar()
            print(f"   {usuario.is_superuser} OR {permiso.puede_editar()} = {condicion}")
            
            if condicion:
                print(f"\n   ✅ BOTONES DEBERÍAN APARECER")
            else:
                print(f"\n   ❌ BOTONES NO APARECERÍAN")
            
            # Asignar al request como lo hace el middleware
            request.permiso_actual = permiso
            
        except Permiso.DoesNotExist:
            print(f"   ❌ PERMISO NO ENCONTRADO")
    else:
        print(f"   ❌ Módulo no encontrado para URL {request.path}")

# 4. Ahora, simular lo que pasa en la vista
print(f"\n\n📋 CONTEXTO PASADO A TEMPLATE:")
print("-" * 120)

# Lo que hace la vista lista_especialidades
permiso = getattr(request, 'permiso_actual', None)
print(f"   permiso_actual: {permiso}")
if permiso:
    print(f"   permiso_actual.puede_editar(): {permiso.puede_editar()}")
    print(f"   user.is_superuser: {request.user.is_superuser}")

# 5. Probar con otros usuarios
print(f"\n\n🔀 PRUEBAS CON OTROS USUARIOS:")
print("-" * 120)

for username in ['encargado', 'julio', 'maria', 'monica']:
    user = User.objects.filter(username=username).first()
    if user:
        request = factory.get('/especialidades/')
        request.user = user
        
        es_admin = es_admin_o_staff(user)
        
        if not es_admin:
            tipo_usuario = user.perfil.tipo
            middleware = PermisosMiddleware(lambda r: None)
            modulo = middleware.obtener_modulo_por_url(request.path)
            
            if modulo:
                try:
                    permiso = Permiso.objects.get(tipo_usuario=tipo_usuario, modulo=modulo)
                    print(f"\n{username} ({tipo_usuario.nombre}):")
                    print(f"   - permiso: {permiso.tipo_permiso}")
                    print(f"   - puede_editar(): {permiso.puede_editar()}")
                    print(f"   - Botones aparecerían: {user.is_superuser or permiso.puede_editar()}")
                except Permiso.DoesNotExist:
                    print(f"\n{username}: ❌ Sin permiso")
            else:
                print(f"\n{username}: ❌ Módulo no encontrado")
        else:
            print(f"\n{username}: ✅ Es admin/staff (acceso total)")

print("\n" + "=" * 120)

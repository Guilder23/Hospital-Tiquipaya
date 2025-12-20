#!/usr/bin/env python
"""
Test interactivo para verificar permisos en tiempo real
Esto ejecuta exactamente lo mismo que hace el sistema
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from django.contrib.auth.models import User
from apps.permisos.models import Permiso, Modulo

# Obtener usuario y módulo
usuario = User.objects.get(username='encargado')
modulo = Modulo.objects.get(nombre='Gestion de Especialidades')

print("\n" + "="*80)
print("TEST EN TIEMPO REAL DEL SISTEMA DE PERMISOS")
print("="*80)

print(f"\n👤 Usuario: {usuario.username}")
print(f"   - is_superuser: {usuario.is_superuser}")
print(f"   - is_staff: {usuario.is_staff}")

print(f"\n📋 Módulo: {modulo.nombre}")

# Obtener permiso
permiso = Permiso.objects.get(tipo_usuario=usuario.perfil.tipo, modulo=modulo)

print(f"\n✅ PERMISO OBTENIDO:")
print(f"   - ID: {permiso.id}")
print(f"   - Tipo permiso: {permiso.tipo_permiso}")
print(f"   - Visible: {permiso.visible}")
print(f"   - puede_editar(): {permiso.puede_editar()}")

# Verificar la condición exacta del template
condicion = usuario.is_superuser or permiso.puede_editar()

print(f"\n🔍 CONDICIÓN DEL TEMPLATE:")
print("   {% if user.is_superuser or permiso_actual.puede_editar %}")
print(f"   = {usuario.is_superuser} OR {permiso.puede_editar()}")
print(f"   = {condicion}")

if condicion:
    print(f"\n✅ ✅ ✅ LOS BOTONES DEBERÍAN APARECER")
else:
    print(f"\n❌ ❌ ❌ LOS BOTONES NO DEBERÍAN APARECER")

print(f"\n" + "="*80)

# Verificar también otros usuarios
print(f"\n🔀 VERIFICACIÓN DE OTROS USUARIOS:")
print(f"-"*80)

for username in ['julio', 'maria']:
    try:
        user = User.objects.get(username=username)
        tipo = user.perfil.tipo
        perm = Permiso.objects.get(tipo_usuario=tipo, modulo=modulo)
        puede = perm.puede_editar()
        print(f"\n{username} ({tipo.nombre}):")
        print(f"   - puede_editar(): {puede}")
        print(f"   - Botones aparecerían: {user.is_superuser or puede}")
    except:
        print(f"\n{username}: Error")

print(f"\n" + "="*80)

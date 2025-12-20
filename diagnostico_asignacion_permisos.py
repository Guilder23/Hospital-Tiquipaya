#!/usr/bin/env python
"""
Diagnóstico detallado de la asignación de permisos.
Muestra exactamente qué está guardado en la BD para cada tipo de usuario.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from apps.permisos.models import Permiso, Modulo
from apps.accounts.models import TipoUsuario
from django.contrib.auth.models import User

print("=" * 100)
print("DIAGNÓSTICO COMPLETO DE ASIGNACIÓN DE PERMISOS")
print("=" * 100)

# 1. Listar todos los tipos de usuario
print("\n📋 TIPOS DE USUARIO EN EL SISTEMA:")
print("-" * 100)
for tipo in TipoUsuario.objects.all():
    print(f"\n  • {tipo.nombre}")
    
    # Para cada tipo, mostrar sus permisos
    permisos = Permiso.objects.filter(tipo_usuario=tipo).select_related('modulo')
    
    print(f"    Total de permisos: {permisos.count()}")
    
    # Agrupar por tipo_permiso
    por_tipo = {
        'editor': [],
        'solo_vista': [],
        'sin_acceso': []
    }
    
    for permiso in permisos:
        por_tipo[permiso.tipo_permiso].append({
            'modulo': permiso.modulo.nombre,
            'visible': permiso.visible,
            'puede_editar': permiso.puede_editar(),
            'tipo_permiso': permiso.tipo_permiso
        })
    
    print(f"\n    📊 RESUMEN POR TIPO DE PERMISO:")
    print(f"      ✅ Editor (puede_editar=True): {len(por_tipo['editor'])} módulos")
    for item in por_tipo['editor']:
        print(f"         • {item['modulo']} - visible={item['visible']}, puede_editar={item['puede_editar']}")
    
    print(f"      👁️  Solo Vista (solo lectura): {len(por_tipo['solo_vista'])} módulos")
    for item in por_tipo['solo_vista']:
        print(f"         • {item['modulo']} - visible={item['visible']}, puede_editar={item['puede_editar']}")
    
    print(f"      ❌ Sin Acceso: {len(por_tipo['sin_acceso'])} módulos")
    for item in por_tipo['sin_acceso']:
        print(f"         • {item['modulo']} - visible={item['visible']}, puede_editar={item['puede_editar']}")

# 2. Mostrar usuarios y sus tipos
print("\n\n👥 USUARIOS EN EL SISTEMA:")
print("-" * 100)
for user in User.objects.filter(is_active=True):
    tipo = getattr(user, 'perfil', None)
    if tipo:
        print(f"\n  {user.username} ({user.get_full_name() or 'Sin nombre'})")
        print(f"    - Tipo: {tipo.tipo.nombre}")
        print(f"    - is_staff: {user.is_staff}")
        print(f"    - is_superuser: {user.is_superuser}")
        
        # Mostrar qué módulos puede editar este usuario
        permisos = Permiso.objects.filter(tipo_usuario=tipo.tipo, tipo_permiso='editor')
        if permisos.exists():
            print(f"    - Módulos con permiso 'editor': {permisos.count()}")
            for permiso in permisos:
                print(f"      ✅ {permiso.modulo.nombre}")

# 3. Diagnosticar problema específico
print("\n\n🔍 DIAGNÓSTICO ESPECÍFICO:")
print("-" * 100)

# Buscar si hay permisos que digan ser "editor" pero sin visible
problematicos = Permiso.objects.filter(tipo_permiso='editor', visible=False)
if problematicos.exists():
    print(f"\n⚠️  PROBLEMA ENCONTRADO: Hay {problematicos.count()} permisos 'editor' con visible=False")
    for p in problematicos:
        print(f"   • {p.tipo_usuario.nombre} - {p.modulo.nombre}: visible={p.visible}, tipo_permiso={p.tipo_permiso}, puede_editar={p.puede_editar()}")
else:
    print("\n✅ No hay permisos 'editor' con visible=False (buen estado)")

# Buscar si hay valores raros en tipo_permiso
valores_tipo = Permiso.objects.values_list('tipo_permiso', flat=True).distinct()
print(f"\n📝 Valores únicos en tipo_permiso: {list(valores_tipo)}")

# 4. Test directo del método puede_editar
print("\n\n🧪 TEST DEL MÉTODO puede_editar():")
print("-" * 100)

tipo_encargado = TipoUsuario.objects.filter(nombre__icontains='Encargado').first()
if tipo_encargado:
    permisos = Permiso.objects.filter(tipo_usuario=tipo_encargado)
    print(f"\nProbando con tipo: {tipo_encargado.nombre}")
    
    for permiso in permisos[:5]:  # Mostrar primeros 5
        resultado = permiso.puede_editar()
        print(f"  Módulo: {permiso.modulo.nombre}")
        print(f"    - visible: {permiso.visible}")
        print(f"    - tipo_permiso: {permiso.tipo_permiso}")
        print(f"    - puede_editar(): {resultado}")
        print(f"    - Condición (visible AND tipo_permiso=='editor'): {permiso.visible and permiso.tipo_permiso == 'editor'}")
        print()

print("\n" + "=" * 100)

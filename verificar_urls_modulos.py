#!/usr/bin/env python
"""
Verificar URLs de módulos en la BD
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from apps.permisos.models import Modulo

print("\n" + "="*100)
print("URLs DE MÓDULOS EN LA BD")
print("="*100)

modulos = Modulo.objects.filter(activo=True).order_by('nombre')

print(f"\n📋 Total de módulos activos: {modulos.count()}\n")

for m in modulos:
    print(f"  • {m.nombre}")
    print(f"    URL: {m.url}")
    
    # Verificar si '/especialidades/' hace match
    if '/especialidades/'.startswith(m.url):
        print(f"    ✅ '/especialidades/'.startswith('{m.url}') = True")
    else:
        print(f"    ❌ '/especialidades/'.startswith('{m.url}') = False")
    
    print()

print("\n" + "="*100)
print("TEST: ¿Cuál módulo coincide con '/especialidades/'?")
print("="*100)

test_path = '/especialidades/'
print(f"\nPath a buscar: {test_path}\n")

for modulo in modulos:
    if test_path.startswith(modulo.url):
        print(f"✅ MATCH ENCONTRADO: {modulo.nombre} (URL: {modulo.url})")
        break
else:
    print(f"❌ NO COINCIDE CON NINGÚN MÓDULO")

print("\n" + "="*100)

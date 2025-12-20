#!/usr/bin/env python
"""
Test exacto de lo que hace obtener_modulo_por_url con /especialidades/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from apps.permisos.middleware import PermisosMiddleware
from apps.permisos.models import Modulo

middleware = PermisosMiddleware(lambda r: None)

test_path = '/especialidades/'
print(f"\n" + "="*100)
print(f"TEST: ¿ obtener_modulo_por_url('{test_path}') retorna qué?")
print("="*100)

modulo = middleware.obtener_modulo_por_url(test_path)

if modulo:
    print(f"\n✅ MÓDULO ENCONTRADO: {modulo.nombre}")
    print(f"   - URL: {modulo.url}")
    print(f"   - Activo: {modulo.activo}")
else:
    print(f"\n❌ NO SE ENCONTRÓ MÓDULO")
    
    # Mostrar todos los módulos activos
    print(f"\nMódulos activos en la BD:")
    modulos = Modulo.objects.filter(activo=True)
    for m in modulos:
        print(f"  • {m.nombre}: {m.url}")
        test_result = test_path.startswith(m.url)
        print(f"    '{test_path}'.startswith('{m.url}') = {test_result}")

print("\n" + "="*100)

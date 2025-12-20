#!/usr/bin/env python
"""
Extraer exactamente el HTML relevante para verificar los botones
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import re

# Login
client = Client()
usuario = User.objects.get(username='encargado')
usuario.set_password('test123')
usuario.save()
client.login(username='encargado', password='test123')

# Request
response = client.get('/especialidades/')
html = response.content.decode('utf-8')

print("\n" + "="*120)
print("DEBUG: ATRIBUTOS DEL DIV PRINCIPAL")
print("="*120)

# Buscar el div con los atributos data
match = re.search(r'<div class="card shadow-sm"[^>]*>', html)
if match:
    div_tag = match.group(0)
    print(f"\n{div_tag[:300]}...")
    
    # Extraer atributos
    attrs = {
        'data-user-superuser': re.search(r'data-user-superuser="([^"]*)"', div_tag),
        'data-permiso-puede-editar': re.search(r'data-permiso-puede-editar="([^"]*)"', div_tag),
        'data-permiso-tipo': re.search(r'data-permiso-tipo="([^"]*)"', div_tag),
        'data-middleware-ejecutado': re.search(r'data-middleware-ejecutado="([^"]*)"', div_tag),
        'data-middleware-razon': re.search(r'data-middleware-razon="([^"]*)"', div_tag),
    }
    
    print(f"\n📊 ATRIBUTOS EXTRAÍDOS:")
    for attr, match_obj in attrs.items():
        if match_obj:
            print(f"  {attr}: {match_obj.group(1)}")
        else:
            print(f"  {attr}: NO ENCONTRADO")

print(f"\n" + "="*120)


#!/usr/bin/env python
"""
Simular request con logging para ver exactamente qué pasa en el middleware
"""

import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

# Configurar logging para ver qué pasa
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

from django.test import Client
from django.contrib.auth.models import User

print("\n" + "="*100)
print("SIMULACIÓN CON LOGGING DETALLADO")
print("="*100)

# Crear cliente
client = Client()

# Login
print(f"\n🔐 Intentando login con usuario 'encargado'...")
usuario = User.objects.get(username='encargado')
usuario.set_password('test123')
usuario.save()

login_ok = client.login(username='encargado', password='test123')
print(f"    {'✅ Login OK' if login_ok else '❌ Login Failed'}")

if login_ok:
    print(f"\n📡 Haciendo request a /especialidades/...")
    print("-"*100)
    
    response = client.get('/especialidades/')
    
    print("-"*100)
    print(f"\n📊 Response status: {response.status_code}")
    
    # Verificar si aparecen los botones
    html = response.content.decode('utf-8')
    
    if 'btn-open-create' in html:
        print(f"✅ Botón 'Nueva Especialidad' SÍ aparece en el HTML")
    else:
        print(f"❌ Botón 'Nueva Especialidad' NO aparece en el HTML")
    
    if 'btn-edit' in html:
        print(f"✅ Botones 'Editar' SÍ aparecen en el HTML")
    else:
        print(f"❌ Botones 'Editar' NO aparecen en el HTML")

print("\n" + "="*100)

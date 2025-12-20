#!/usr/bin/env python
"""
Test final: Verificar que el sistema funciona para todos los tipos de usuarios
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from apps.accounts.models import Perfil, TipoUsuario
from apps.permisos.models import Permiso

print("\n" + "="*120)
print("TEST FINAL: SISTEMA DE PERMISOS - TODOS LOS USUARIOS")
print("="*120)

client = Client()

# Preparar usuarios
usuarios = [
    ('encargado', 'test123'),      # Encargado de Admision - "editor"
    ('maria', 'test123'),          # Recepcion de Admision - "solo_vista"
    ('julio', 'test123'),          # Ecografo - "sin_acceso"
]

# Preparar contraseñas
for username, password in usuarios:
    user = User.objects.filter(username=username).first()
    if user:
        user.set_password(password)
        user.save()

print(f"\n📝 Usuarios a probar: {[u[0] for u in usuarios]}")

# Test por usuario
for username, password in usuarios:
    user = User.objects.filter(username=username).first()
    if not user:
        print(f"\n❌ Usuario {username} no encontrado")
        continue
    
    print(f"\n" + "-"*120)
    print(f"👤 Usuario: {username}")
    print(f"   Tipo: {user.perfil.tipo.nombre}")
    
    # Login
    login_ok = client.login(username=username, password=password)
    if not login_ok:
        print(f"   ❌ No se pudo hacer login")
        continue
    
    # Test endpoints
    endpoints = [
        ('/especialidades/', 'Gestion de Especialidades'),
        ('/pacientes/', 'Gestionar Pacientes'),
        ('/turnos/', 'Gestion de Turnos'),
    ]
    
    for url, modulo_nombre in endpoints:
        try:
            # Obtener permiso esperado
            tipo = user.perfil.tipo
            permiso = Permiso.objects.filter(
                tipo_usuario=tipo,
                modulo__nombre__icontains=modulo_nombre.split()[0]
            ).first()
            
            if permiso:
                tipo_permiso = permiso.tipo_permiso
                puede_editar = permiso.puede_editar()
                
                # Hacer request
                response = client.get(url)
                html = response.content.decode('utf-8')
                
                # Verificar botones
                tiene_btn_editar = 'btn-edit' in html
                
                print(f"\n   {url}")
                print(f"      Permiso esperado: {tipo_permiso} (puede_editar={puede_editar})")
                print(f"      Botones en HTML: {'btn-edit' if tiene_btn_editar else 'solo btn-view'}")
                
                # Verificación
                if tipo_permiso == 'editor' and puede_editar:
                    if tiene_btn_editar:
                        print(f"      ✅ CORRECTO: Editor y botones presentes")
                    else:
                        print(f"      ❌ ERROR: Editor pero botones ausentes")
                elif tipo_permiso == 'solo_vista':
                    if not tiene_btn_editar:
                        print(f"      ✅ CORRECTO: Solo vista y sin botones de edición")
                    else:
                        print(f"      ❌ ERROR: Solo vista pero tiene botones de edición")
                elif tipo_permiso == 'sin_acceso':
                    print(f"      ℹ️  Sin acceso (respuesta {response.status_code})")
            else:
                print(f"\n   {url}")
                print(f"      ℹ️  No hay permiso configurado para este módulo")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    client.logout()

print(f"\n" + "="*120)
print("TEST COMPLETADO")
print("="*120 + "\n")

#!/usr/bin/env python
"""
Verifica exactamente lo que genera el servidor para /especialidades/
Simula una request HTTP real y revisa el HTML resultante
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from apps.especialidades.views import lista_especialidades
from apps.permisos.middleware import PermisosMiddleware
from apps.permisos.models import Permiso, Modulo
import re

print("\n" + "="*100)
print("VERIFICACIÓN DE SALIDA HTML - /especialidades/")
print("="*100)

# Crear cliente y usuario
client = Client()
usuario = User.objects.get(username='encargado')

print(f"\n👤 Usuario: {usuario.username}")
print(f"   - is_superuser: {usuario.is_superuser}")
print(f"   - is_staff: {usuario.is_staff}")

# Login
login_ok = client.login(username='encargado', password='encargado123')
print(f"\n🔐 Login: {'✅' if login_ok else '❌'}")

if not login_ok:
    print("⚠️  Intentando con otra contraseña...")
    # Intentar con contraseña genérica
    from django.contrib.auth.hashers import make_password
    usuario.set_password('test123')
    usuario.save()
    login_ok = client.login(username='encargado', password='test123')
    print(f"🔐 Login con nueva contraseña: {'✅' if login_ok else '❌'}")

if login_ok:
    # Hacer request a /especialidades/
    response = client.get('/especialidades/')
    
    print(f"\n📡 Response status: {response.status_code}")
    
    if response.status_code == 200:
        html = response.content.decode('utf-8')
        
        # Buscar atributos de debug
        print("\n🔍 ATRIBUTOS DE DEBUG EN HTML:")
        
        match_superuser = re.search(r'data-user-superuser="([^"]*)"', html)
        match_puede_editar = re.search(r'data-permiso-puede-editar="([^"]*)"', html)
        match_tipo_permiso = re.search(r'data-permiso-tipo="([^"]*)"', html)
        
        if match_superuser:
            print(f"   - data-user-superuser: {match_superuser.group(1)}")
        if match_puede_editar:
            print(f"   - data-permiso-puede-editar: {match_puede_editar.group(1)}")
        if match_tipo_permiso:
            print(f"   - data-permiso-tipo: {match_tipo_permiso.group(1)}")
        
        # Buscar botones de acción
        print(f"\n🔘 BOTONES EN HTML:")
        
        btn_create = re.search(r'id="btn-open-create"', html)
        btn_edit_count = len(re.findall(r'btn-edit', html))
        btn_view_count = len(re.findall(r'btn-view', html))
        btn_danger_count = len(re.findall(r'btn-danger', html))
        
        print(f"   - Botón 'Nueva Especialidad': {'✅ ENCONTRADO' if btn_create else '❌ NO ENCONTRADO'}")
        print(f"   - Botones 'Editar': {btn_edit_count} encontrados")
        print(f"   - Botones 'Ver': {btn_view_count} encontrados")
        print(f"   - Botones 'Desactivar': {btn_danger_count} encontrados")
        
        # Condicional que está evaluando Django
        print(f"\n📋 ANÁLISIS DE CONDICIONALES:")
        
        # Buscar secciones condicionales
        if_condicional = re.search(
            r'<\!-- Botón abrir modal custom -->\s*'
            r'({% if user\.is_superuser or permiso_actual\.puede_editar %}.*?{% endif %})',
            html,
            re.DOTALL
        )
        
        if if_condicional:
            contenido = if_condicional.group(1)[:200]  # Primeros 200 caracteres
            print(f"   ✅ Condicional encontrada")
            if 'btn-open-create' in contenido:
                print(f"   ✅ El botón está DENTRO del condicional (se muestra porque es True)")
            else:
                print(f"   ❌ El botón NO está dentro del condicional (se omite porque es False)")
        
        # Verificación final
        print(f"\n✅ CONCLUSIÓN:")
        if btn_create:
            print(f"   El servidor SÍ genera el botón 'Nueva Especialidad'")
            print(f"   El condicional 'user.is_superuser or permiso_actual.puede_editar' fue TRUE")
        else:
            print(f"   El servidor NO genera el botón 'Nueva Especialidad'")
            print(f"   El condicional 'user.is_superuser or permiso_actual.puede_editar' fue FALSE")
        
        if btn_edit_count > 0:
            print(f"   El servidor SÍ genera los botones 'Editar' ({btn_edit_count} encontrados)")
        else:
            print(f"   El servidor NO genera los botones 'Editar'")
    
    else:
        print(f"❌ Error: Status {response.status_code}")
        if response.status_code == 302:
            print(f"   Redirección a: {response.get('Location')}")
        
else:
    print("\n❌ No se pudo hacer login")
    print("\nIntentando obtener usuario y verificar direc tamente...")
    
    # Simulación sin cliente
    factory = RequestFactory()
    request = factory.get('/especialidades/')
    request.user = usuario
    
    tipo_usuario = usuario.perfil.tipo
    modulo = Modulo.objects.get(nombre='Gestion de Especialidades')
    permiso = Permiso.objects.get(tipo_usuario=tipo_usuario, modulo=modulo)
    
    request.permiso_actual = permiso
    
    print(f"\nPermisos directos:")
    print(f"   - user.is_superuser: {usuario.is_superuser}")
    print(f"   - permiso_actual.puede_editar(): {permiso.puede_editar()}")
    print(f"   - Condición sería: {usuario.is_superuser or permiso.puede_editar()}")

print("\n" + "="*100)

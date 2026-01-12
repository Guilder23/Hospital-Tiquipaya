#!/usr/bin/env python
"""
Script para exportar datos de módulos y permisos como comandos SQL
Ejecutar con: python exportar_permisos.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from apps.permisos.models import Modulo, Permiso
from apps.accounts.models import TipoUsuario

print("-- ============================================")
print("-- SCRIPT DE DATOS PARA MÓDULOS Y PERMISOS")
print("-- ============================================\n")

# Exportar TipoUsuario primero
print("-- Tipos de Usuario")
for tipo in TipoUsuario.objects.all().order_by('id'):
    print(f"INSERT INTO accounts_tipousuario (id, nombre, descripcion, creado_en, actualizado_en) VALUES ({tipo.id}, '{tipo.nombre}', '{tipo.descripcion}', NOW(), NOW()) ON CONFLICT (id) DO NOTHING;")

print("\n-- Módulos")
for modulo in Modulo.objects.all().order_by('orden', 'id'):
    nombre = modulo.nombre.replace("'", "''")
    desc = (modulo.descripcion or '').replace("'", "''")
    icono = (modulo.icono or '').replace("'", "''")
    url = modulo.url.replace("'", "''")
    padre = f"{modulo.modulo_padre_id}" if modulo.modulo_padre_id else "NULL"
    
    print(f"INSERT INTO permisos_modulo (id, nombre, descripcion, icono, url, orden, activo, asignable, modulo_padre_id) ")
    print(f"VALUES ({modulo.id}, '{nombre}', '{desc}', '{icono}', '{url}', {modulo.orden}, {modulo.activo}, {modulo.asignable}, {padre}) ")
    print(f"ON CONFLICT (id) DO UPDATE SET nombre=EXCLUDED.nombre, url=EXCLUDED.url, icono=EXCLUDED.icono, orden=EXCLUDED.orden;")

print("\n-- Roles por Defecto (relación many-to-many)")
for modulo in Modulo.objects.all():
    for role in modulo.roles_por_defecto.all():
        print(f"INSERT INTO permisos_modulo_roles_por_defecto (modulo_id, tipousuario_id) VALUES ({modulo.id}, {role.id}) ON CONFLICT DO NOTHING;")

print("\n-- Permisos")
for permiso in Permiso.objects.all().select_related('tipo_usuario', 'modulo'):
    print(f"INSERT INTO permisos_permiso (tipo_usuario_id, modulo_id, tipo_permiso, visible) ")
    print(f"VALUES ({permiso.tipo_usuario_id}, {permiso.modulo_id}, '{permiso.tipo_permiso}', {permiso.visible}) ")
    print(f"ON CONFLICT (tipo_usuario_id, modulo_id) DO UPDATE SET tipo_permiso=EXCLUDED.tipo_permiso, visible=EXCLUDED.visible;")

print("\n-- ============================================")
print("-- FIN DEL SCRIPT")
print("-- ============================================")

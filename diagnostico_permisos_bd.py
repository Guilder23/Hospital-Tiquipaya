"""
Diagnóstico: Revisar qué permisos están en la BD
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_tiquipaya.settings')
django.setup()

from apps.accounts.models import TipoUsuario
from apps.permisos.models import Permiso, Modulo

print("=" * 100)
print("DIAGNÓSTICO: PERMISOS EN BASE DE DATOS")
print("=" * 100)

# Obtener Encargado de Admisión
tipo = TipoUsuario.objects.filter(nombre__icontains="Encargado").first()

if tipo:
    print(f"\n👤 Tipo de Usuario: {tipo.nombre}")
    
    # Obtener todos sus permisos
    permisos = Permiso.objects.filter(tipo_usuario=tipo).select_related('modulo')
    
    print(f"\n📋 Permisos asignados (total: {permisos.count()}):")
    print(f"\n{'Módulo':<40} {'Visible':<10} {'Tipo Permiso':<15} {'Puede Editar':<15}")
    print("─" * 80)
    
    for permiso in permisos:
        puede_editar = "✅ SÍ" if permiso.puede_editar() else "❌ NO"
        visible = "✅ SÍ" if permiso.visible else "❌ NO"
        
        print(f"{permiso.modulo.nombre:<40} {visible:<10} {permiso.tipo_permiso:<15} {puede_editar:<15}")
    
    print("\n" + "=" * 100)
    print("VERIFICACIÓN DE MÓDULOS 'POR DEFECTO'")
    print("=" * 100)
    
    modulos_por_defecto = tipo.modulos_por_defecto.all()
    
    if modulos_por_defecto.exists():
        print(f"\n✅ Módulos 'Por Defecto' para {tipo.nombre}:")
        for modulo in modulos_por_defecto:
            # Obtener el permiso para este módulo
            permiso = Permiso.objects.filter(tipo_usuario=tipo, modulo=modulo).first()
            if permiso:
                puede_editar = "✅ SÍ" if permiso.puede_editar() else "❌ NO"
                print(f"   • {modulo.nombre} → {permiso.tipo_permiso} ({puede_editar})")
            else:
                print(f"   • {modulo.nombre} → SIN PERMISO")
    else:
        print(f"\n❌ Sin módulos 'por defecto'")
    
    print("\n" + "=" * 100)
    print("MÓDULOS QUE DEBERÍA VER")
    print("=" * 100)
    
    permisos_visibles = permisos.filter(visible=True).exclude(tipo_permiso='sin_acceso')
    
    print(f"\n✅ Módulos visibles en sidebar:")
    for permiso in permisos_visibles:
        estado = "📝 EDITOR" if permiso.puede_editar() else "👁️ SOLO VISTA"
        print(f"   • {permiso.modulo.nombre} → {estado}")

print("\n")

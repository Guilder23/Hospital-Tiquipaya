from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Modulo, Permiso
from apps.accounts.models import TipoUsuario


def es_administrador(user):
    """Verifica si el usuario es administrador"""
    if user.is_superuser:
        return True
    try:
        return user.perfil.tipo and user.perfil.tipo.nombre == 'Administrador'
    except:
        return False


@login_required
@user_passes_test(es_administrador)
def listar_tipos(request):
    """Vista para listar tipos de usuario y gestionar permisos"""
    tipos = TipoUsuario.objects.all().order_by('nombre')
    return render(request, 'permisos/tipos.html', {
        'tipos': tipos
    })


@login_required
@user_passes_test(es_administrador)
def asignar_permisos(request, tipo_id):
    """Vista para asignar permisos a un tipo de usuario (estilo matriz)"""
    tipo = get_object_or_404(TipoUsuario, id=tipo_id)
    # Solo mostrar módulos principales (excluir gestión interna)
    modulos_excluidos = ['Usuarios', 'Tipos de Usuario', 'Gestión de Permisos']
    modulos = Modulo.objects.filter(activo=True).exclude(nombre__in=modulos_excluidos).order_by('orden', 'nombre')
    
    # Obtener módulos por defecto para este tipo
    modulos_por_defecto = set(tipo.modulos_por_defecto.values_list('id', flat=True))
    
    if request.method == 'POST':
        # Procesar cada módulo
        for modulo in modulos:
            # Si es un módulo por defecto, siempre debe ser visible
            if modulo.id in modulos_por_defecto:
                visible = True
                tipo_permiso = request.POST.get(f'permiso_{modulo.id}', 'editor')
            else:
                visible = request.POST.get(f'visible_{modulo.id}') == 'on'
                tipo_permiso = request.POST.get(f'permiso_{modulo.id}', 'sin_acceso')
                
                # Si no es visible, forzar sin_acceso
                if not visible:
                    tipo_permiso = 'sin_acceso'
            
            # Crear o actualizar permiso
            Permiso.objects.update_or_create(
                tipo_usuario=tipo,
                modulo=modulo,
                defaults={
                    'visible': visible,
                    'tipo_permiso': tipo_permiso
                }
            )
        
        messages.success(request, f'Permisos del tipo "{tipo.nombre}" actualizados exitosamente')
        return redirect('permisos:listar_tipos')
    
    # Obtener permisos actuales
    permisos_dict = {}
    for permiso in Permiso.objects.filter(tipo_usuario=tipo).select_related('modulo'):
        permisos_dict[permiso.modulo.id] = permiso
    
    return render(request, 'permisos/asignar.html', {
        'tipo': tipo,
        'modulos': modulos,
        'permisos_dict': permisos_dict,
        'modulos_por_defecto': modulos_por_defecto
    })

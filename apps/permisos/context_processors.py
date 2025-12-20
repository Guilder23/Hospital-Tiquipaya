from .models import Permiso, Modulo


def permisos_usuario(request):
    """Context processor para agregar permisos del usuario a todos los templates"""
    context = {
        'modulos_sidebar': [],
        'tipo_usuario': None,
        'tiene_permiso_admin': False,
    }
    
    if request.user.is_authenticated:
        # Superusuarios tienen todos los permisos
        if request.user.is_superuser:
            context['tiene_permiso_admin'] = True
            modulos = Modulo.objects.filter(activo=True).order_by('orden')
            context['modulos_sidebar'] = [
                {
                    'nombre': m.nombre,
                    'url': m.url,
                    'icono': m.icono,
                    'puede_editar': True,
                    'es_solo_vista': False
                }
                for m in modulos
            ]
            return context
        
        try:
            # Obtener tipo de usuario desde el perfil
            tipo_usuario = request.user.perfil.tipo
            context['tipo_usuario'] = tipo_usuario
            
            if not tipo_usuario:
                return context
            
            # Obtener módulos por defecto para este tipo
            modulos_por_defecto = tipo_usuario.modulos_por_defecto.filter(activo=True)
            
            # Obtener permisos visibles del usuario
            permisos = Permiso.objects.filter(
                tipo_usuario=tipo_usuario,
                visible=True,
                modulo__activo=True
            ).select_related('modulo').exclude(
                tipo_permiso='sin_acceso'
            ).order_by('modulo__orden')
            
            # Excluir módulos de gestión interna
            modulos_excluidos = ['Usuarios', 'Gestión de Permisos']
            
            # Construir lista de módulos (permisos + módulos por defecto)
            modulos_dict = {}
            
            # Primero agregar permisos asignados
            for permiso in permisos:
                if permiso.modulo.nombre not in modulos_excluidos:
                    modulos_dict[permiso.modulo.id] = {
                        'nombre': permiso.modulo.nombre,
                        'url': permiso.modulo.url,
                        'icono': permiso.modulo.icono,
                        'puede_editar': permiso.puede_editar(),
                        'es_solo_vista': permiso.es_solo_vista()
                    }
            
            # Agregar módulos por defecto (aunque no tengan permiso asignado)
            for modulo in modulos_por_defecto:
                if modulo.nombre not in modulos_excluidos and modulo.id not in modulos_dict:
                    # Si no tiene permiso asignado, usar como editor por defecto
                    modulos_dict[modulo.id] = {
                        'nombre': modulo.nombre,
                        'url': modulo.url,
                        'icono': modulo.icono,
                        'puede_editar': True,
                        'es_solo_vista': False
                    }
            
            # Ordenar por orden del módulo
            modulos_ordenados = sorted(modulos_dict.values(), key=lambda x: x['nombre'])
            context['modulos_sidebar'] = modulos_ordenados
            
            # Verificar si tiene permiso para gestionar permisos (tipo Administrador)
            if tipo_usuario.nombre == 'Administrador':
                context['tiene_permiso_admin'] = True
        
        except AttributeError:
            # Usuario sin perfil
            pass
    
    return context

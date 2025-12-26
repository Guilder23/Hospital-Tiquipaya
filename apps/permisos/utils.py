from apps.accounts.models import Perfil, TipoUsuario


def obtener_primer_modulo_usuario(user):
    """
    Obtiene la URL del primer módulo disponible para el usuario según sus permisos.
    Retorna None si no tiene módulos disponibles.
    """
    if not user.is_authenticated:
        return None
    
    # Superusers go to dashboard
    if user.is_superuser:
        return '/dashboard/'
    
    try:
        if not hasattr(user, 'perfil') or not user.perfil or not user.perfil.tipo:
            return None
        
        tipo_usuario = user.perfil.tipo
        
        # Import here to avoid circular imports
        from apps.permisos.models import Permiso, Modulo
        
        # Get visible permissions ordered by module order
        permisos = Permiso.objects.filter(
            tipo_usuario=tipo_usuario,
            visible=True,
            modulo__activo=True
        ).exclude(tipo_permiso='sin_acceso').select_related('modulo').order_by('modulo__orden')
        
        # Get default modules for this role
        modulos_por_defecto = tipo_usuario.modulos_por_defecto.filter(activo=True).order_by('orden')
        
        # Combine and get the first one (by order)
        primer_modulo = None
        primer_orden = float('inf')
        
        # Check permissions first
        for permiso in permisos:
            if permiso.modulo.orden < primer_orden:
                primer_orden = permiso.modulo.orden
                primer_modulo = permiso.modulo
        
        # Check default modules
        for modulo in modulos_por_defecto:
            if modulo.orden < primer_orden:
                primer_orden = modulo.orden
                primer_modulo = modulo
        
        if primer_modulo:
            return primer_modulo.url
        
        return None
        
    except (AttributeError, Perfil.DoesNotExist):
        return None


def es_admin_o_staff(user):
    """
    Verifica si el usuario es ADMINISTRADOR del sistema (acceso total).
    
    Solo retorna True para:
    - Superusuario de Django (is_superuser=True)
    - Usuario con is_staff=True Y tipo='Administrador'
    
    Los demás usuarios (Médicos, Recepcionistas, etc.) usan permisos específicos.
    """
    if not user.is_authenticated:
        return False
    
    # Verificar si es superusuario
    if user.is_superuser:
        return True
    
    # Verificar si es staff Y su tipo es "Administrador"
    if user.is_staff:
        try:
            perfil = user.perfil
            if perfil.tipo and perfil.tipo.nombre == 'Administrador':
                return True
        except (AttributeError, Perfil.DoesNotExist):
            pass
    
    return False


class PermisoAdmin:
    """Permiso virtual para administradores/staff que permite todo"""
    
    def puede_editar(self):
        return True
    
    def tiene_acceso(self):
        return True
    
    def es_solo_vista(self):
        return False
    
    def __str__(self):
        return "Permiso Admin (Acceso Total)"


def obtener_permiso_para_usuario(user):
    """
    Obtiene el objeto de permiso para un usuario.
    Si es admin/staff, retorna un PermisoAdmin virtual.
    """
    if es_admin_o_staff(user):
        return PermisoAdmin()
    
    # Si no es admin, intenta obtener su permiso normal
    try:
        perfil = user.perfil
        if perfil.tipo:
            # Retornar un objeto que indica que no tiene permiso
            return None
    except (AttributeError, Perfil.DoesNotExist):
        pass
    
    return None

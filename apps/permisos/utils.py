from apps.accounts.models import Perfil, TipoUsuario


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

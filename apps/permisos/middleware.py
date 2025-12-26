from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve
from .models import Permiso, Modulo
from .utils import es_admin_o_staff, PermisoAdmin
import logging

logger = logging.getLogger(__name__)


class PermisosMiddleware:
    """Middleware para validar permisos en cada request"""
    
    RUTAS_PUBLICAS = [
        '/admin/',
        '/accounts/login/',
        '/accounts/logout/',
        '/static/',
        '/media/',
        '/citas/agendar/',
        '/citas/validar/',
        '/citas/agenda/',
        '/citas/confirmar/',
        '/citas/logout/',
    ]
    
    # Rutas que no requieren validación de permisos (específicas de usuarios autenticados)
    RUTAS_SIN_VALIDACION = [
        '/citas/medico/hoy/',
        '/citas/medico/atendidos/',
        '/citas-ecografia/mis-citas/',
        '/citas-ecografia/pacientes-atendidos/',
        '/citas/agendar-usuario/',
        '/citas/buscar-paciente/',
        '/citas/confirmar-usuario/',
    ]
    
    # Rutas para pacientes (requieren sesión de paciente, no autenticación de Django)
    RUTAS_PACIENTE = [
        '/citas/mis/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Permitir rutas públicas y la home específicamente
        if request.path == '/' or any(request.path.startswith(ruta) for ruta in self.RUTAS_PUBLICAS):
            return self.get_response(request)
        
        # IMPORTANTE: Verificar rutas específicas ANTES que las genéricas
        # Rutas que no requieren validación de permisos (para usuarios autenticados)
        if any(request.path.startswith(ruta) for ruta in self.RUTAS_SIN_VALIDACION):
            if request.user.is_authenticated:
                return self.get_response(request)
            else:
                # Si no está autenticado, redirigir a login
                messages.warning(request, 'Debes iniciar sesión para acceder a esta sección')
                return redirect('login')
        
        # Rutas dinámicas de citas (verificar primero si es ruta de paciente o de médico)
        if request.path.startswith('/citas/') and any(char.isdigit() for char in request.path):
            # Verificar si es una ruta de paciente (cancelar, editar, pdf, orden)
            if any(segment in request.path for segment in ['/cancelar/', '/editar/', '/pdf/', '/orden/']):
                # Permitir si tiene sesión de paciente o está autenticado
                if request.session.get('paciente_id') or request.user.is_authenticated:
                    return self.get_response(request)
                else:
                    messages.info(request, 'Debes validar tus datos como paciente primero')
                    return redirect('home')
            # Si no es ruta de paciente, requiere autenticación Django (médicos)
            elif request.user.is_authenticated:
                return self.get_response(request)
            else:
                messages.warning(request, 'Debes iniciar sesión para acceder')
                return redirect('login')
        
        # Rutas para pacientes (mis citas, etc - rutas sin ID)
        if any(request.path.startswith(ruta) for ruta in self.RUTAS_PACIENTE):
            # Verificar si tiene sesión de paciente
            if request.session.get('paciente_id'):
                return self.get_response(request)
            # Si está autenticado como usuario del sistema, también permitir
            elif request.user.is_authenticated:
                return self.get_response(request)
            else:
                # Si no tiene sesión de paciente ni está autenticado, redirigir a home
                messages.info(request, 'Debes validar tus datos como paciente primero')
                return redirect('home')
        
        # Si es superusuario o admin/staff, crear un permiso virtual que permite editar todo
        if request.user.is_authenticated and es_admin_o_staff(request.user):
            request.permiso_actual = PermisoAdmin()
            logger.info(f"✓ Admin/Staff: {request.user.username} → PermisoAdmin asignado")
            return self.get_response(request)
        
        # Verificar permisos si el usuario está autenticado
        if request.user.is_authenticated:
            try:
                # Obtener tipo de usuario desde el perfil
                tipo_usuario = request.user.perfil.tipo
                logger.info(f"🔍 Request: {request.path} | Usuario: {request.user.username} | Tipo: {tipo_usuario}")
                
                if not tipo_usuario:
                    if not request.path.startswith('/permisos/'):
                        messages.warning(request, 'No tienes un tipo de usuario asignado. Contacta al administrador.')
                        return redirect('home')
                
                # Buscar módulo que coincida con la URL
                modulo = self.obtener_modulo_por_url(request.path)
                logger.info(f"  ➜ Módulo encontrado: {modulo.nombre if modulo else 'None'}")
                
                if modulo:
                    try:
                        permiso = Permiso.objects.get(tipo_usuario=tipo_usuario, modulo=modulo)
                        logger.info(f"  ➜ Permiso: {permiso.tipo_permiso}, visible={permiso.visible}")
                        
                        # Verificar si tiene acceso
                        if not permiso.tiene_acceso():
                            messages.error(request, f'No tienes permiso para acceder a {modulo.nombre}')
                            logger.warning(f"  [DENY] Sin acceso a {modulo.nombre}")
                            return redirect('home')
                        
                        # Verificar si es método de modificación y solo tiene vista
                        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH'] and permiso.es_solo_vista():
                            messages.error(request, f'Solo tienes permiso de lectura en {modulo.nombre}')
                            logger.warning(f"  [READ-ONLY] Solo lectura en {modulo.nombre}")
                            return redirect('home')
                        
                        # Agregar el permiso al request para uso en templates
                        request.permiso_actual = permiso
                        logger.info(f"✓ Permiso asignado: {tipo_usuario.nombre} → {modulo.nombre} = {permiso.tipo_permiso}")
                        
                    except Permiso.DoesNotExist:
                        # Si no existe permiso específico, denegar acceso
                        messages.error(request, f'No tienes permiso configurado para acceder a este módulo')
                        logger.error(f"  [ERROR] Permiso no existe para {tipo_usuario} → {modulo}")
                        return redirect('home')
                else:
                    logger.warning(f"  [WARNING] No se encontró módulo para {request.path}")
                
            except AttributeError:
                # Usuario sin perfil
                if not request.path.startswith('/permisos/'):
                    messages.warning(request, 'No tienes un perfil configurado. Contacta al administrador.')
                    logger.error(f"  [ERROR] Usuario sin perfil: {request.user.username}")
                    return redirect('home')
        
        response = self.get_response(request)
        return response
    
    def obtener_modulo_por_url(self, path):
        """Obtiene el módulo basándose en la URL"""
        # Intentar coincidencia exacta primero
        modulos = Modulo.objects.filter(activo=True)
        
        for modulo in modulos:
            if path.startswith(modulo.url):
                return modulo
        
        return None

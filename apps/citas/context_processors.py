from apps.pacientes.models import Paciente

def paciente(request):
    pid = request.session.get('paciente_id')
    obj = None
    if pid:
        try:
            obj = Paciente.objects.get(id=pid)
            print(f"[CONTEXT] Paciente encontrado: {obj.nombres} (ID: {pid})")
        except Paciente.DoesNotExist:
            print(f"[CONTEXT] Paciente ID {pid} no existe, limpiando sesión")
            request.session.pop('paciente_id', None)
    else:
        print("[CONTEXT] No hay paciente_id en sesión")
    return {'paciente': obj}


def user_roles(request):
    """Agregar información de roles del usuario al contexto"""
    context = {}
    
    if request.user.is_authenticated:
        # Verificar si es personal de admisión
        try:
            context['is_admision'] = hasattr(request.user, 'admision') and request.user.admision is not None
        except:
            context['is_admision'] = False
        
        # Verificar si es médico
        try:
            context['is_medico'] = hasattr(request.user, 'medico') and request.user.medico is not None
        except:
            context['is_medico'] = False
    else:
        context['is_admision'] = False
        context['is_medico'] = False
    
    return context

from apps.pacientes.models import Paciente

def paciente(request):
    pid = request.session.get('paciente_id')
    obj = None
    if pid:
        try:
            obj = Paciente.objects.get(id=pid)
        except Paciente.DoesNotExist:
            request.session.pop('paciente_id', None)
    return {'paciente': obj}


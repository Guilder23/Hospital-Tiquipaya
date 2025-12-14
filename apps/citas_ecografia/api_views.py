from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.accounts.models import Ecografo


@login_required
def api_ecografo_info(request, ecografo_id):
    """API para obtener información del ecógrafo"""
    try:
        ecografo = Ecografo.objects.select_related('dias_atencion', 'user__perfil__contrato').prefetch_related('turnos').get(id=ecografo_id)
        
        # Obtener contrato si existe
        contrato = None
        nombres = ""
        if hasattr(ecografo, 'user') and hasattr(ecografo.user, 'perfil'):
            nombres = f"{ecografo.user.perfil.nombres} {ecografo.user.perfil.apellido_paterno}"
            if hasattr(ecografo.user.perfil, 'contrato') and ecografo.user.perfil.contrato:
                contrato = ecografo.user.perfil.contrato
        
        # Días de trabajo en formato número (0=lunes, 6=domingo)
        dias_trabajo = []
        dias_trabajo_numeros = []
        if ecografo.dias_atencion:
            dias_atencion = ecografo.dias_atencion
            if dias_atencion.lunes:
                dias_trabajo.append('Lunes')
                dias_trabajo_numeros.append(0)
            if dias_atencion.martes:
                dias_trabajo.append('Martes')
                dias_trabajo_numeros.append(1)
            if dias_atencion.miercoles:
                dias_trabajo.append('Miércoles')
                dias_trabajo_numeros.append(2)
            if dias_atencion.jueves:
                dias_trabajo.append('Jueves')
                dias_trabajo_numeros.append(3)
            if dias_atencion.viernes:
                dias_trabajo.append('Viernes')
                dias_trabajo_numeros.append(4)
            if dias_atencion.sabado:
                dias_trabajo.append('Sábado')
                dias_trabajo_numeros.append(5)
            if dias_atencion.domingo:
                dias_trabajo.append('Domingo')
                dias_trabajo_numeros.append(6)
        
        # Turnos en formato serializable
        turnos = []
        for turno in ecografo.turnos.all():
            turnos.append({
                'id': turno.id,
                'nombre': turno.nombre,
                'hora_ini': str(turno.hora_ini),
                'hora_fin': str(turno.hora_fin),
                'estado': turno.estado,
            })
        
        return JsonResponse({
            'id': ecografo.id,
            'nombre': nombres,
            'contrato_inicio': contrato.fecha_inicio.isoformat() if contrato else None,
            'contrato_fin': contrato.fecha_fin.isoformat() if contrato else None,
            'dias_trabajo': dias_trabajo,
            'dias_trabajo_numeros': dias_trabajo_numeros,
            'turnos': turnos,
        })
    except Ecografo.DoesNotExist:
        return JsonResponse({
            'error': 'Ecógrafo no encontrado'
        }, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e)
        }, status=500)

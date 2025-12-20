from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from django.conf import settings
from datetime import datetime, timedelta
import logging
import traceback

from apps.pacientes.models import Paciente
from apps.citas.models import Cita
from apps.citas_ecografia.models import CitaEcografia
from apps.accounts.models import Medico, Perfil
from apps.especialidades.models import Especialidad
from apps.contratos.models import Contrato

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    # Verificar si es admin
    if not request.user.is_staff:
        return render(request, 'dashboard/no_acceso.html')
    
    context = {}
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def get_dashboard_data(request):
    """API para obtener datos del dashboard en JSON"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    try:
        # PACIENTES
        total_pacientes = Paciente.objects.count()
        pacientes_activos = Paciente.objects.filter(
            cita__estado='PROGRAMADA'
        ).distinct().count()
        
        # CITAS (Consultas)
        total_citas = Cita.objects.count()
        citas_hoy = Cita.objects.filter(fecha=datetime.now().date()).count()
        citas_programadas = Cita.objects.filter(estado='PROGRAMADA').count()
        citas_canceladas = Cita.objects.filter(estado='CANCELADA').count()
        citas_completadas = Cita.objects.filter(estado_atencion='ATENDIDO').count()
        
        # CITAS POR ESTADO
        citas_por_estado = dict(
            Cita.objects.values('estado').annotate(count=Count('id')).values_list('estado', 'count')
        )
        
        # CITAS POR TIPO
        citas_por_tipo = dict(
            Cita.objects.values('tipo_cita').annotate(count=Count('id')).values_list('tipo_cita', 'count')
        )
        
        # ECOGRAFÍAS (Citas de Ecografía)
        total_ecografias = CitaEcografia.objects.count()
        ecografias_realizadas = CitaEcografia.objects.filter(estado_atencion='ATENDIDO').count()
        ecografias_pendientes = CitaEcografia.objects.filter(estado='PROGRAMADA').count()
        
        # MÉDICOS
        total_medicos = Medico.objects.count()
        medicos_con_turnos = Medico.objects.filter(turnos__isnull=False).distinct().count()
        
        # ESPECIALIDADES
        total_especialidades = Especialidad.objects.count()
        
        # CITAS POR ESPECIALIDAD
        citas_por_especialidad = list(
            Cita.objects.values('especialidad__nombre')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
        
        # CITAS POR MÉDICO (Top 5)
        citas_por_medico = list(
            Cita.objects.values('medico__user__first_name', 'medico__user__last_name')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
        
        # PACIENTES POR GÉNERO
        pacientes_por_genero = dict(
            Paciente.objects.values('genero').annotate(count=Count('id')).values_list('genero', 'count')
        )
        
        # PACIENTES POR SEGURO
        pacientes_con_seguro = Paciente.objects.filter(tiene_seguro=True).count()
        pacientes_sin_seguro = Paciente.objects.filter(tiene_seguro=False).count()
        
        # CONTRATOS
        total_contratos = Contrato.objects.count()
        contratos_vigentes = Contrato.objects.filter(
            fecha_inicio__lte=datetime.now().date(),
            fecha_fin__gte=datetime.now().date()
        ).count()
        
        # ESTADÍSTICAS DE TIEMPO
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        
        citas_este_mes = Cita.objects.filter(
            fecha__month=mes_actual,
            fecha__year=año_actual
        ).count()
        
        # Mes pasado
        if mes_actual == 1:
            mes_pasado = 12
            año_pasado = año_actual - 1
        else:
            mes_pasado = mes_actual - 1
            año_pasado = año_actual
        
        citas_mes_pasado = Cita.objects.filter(
            fecha__month=mes_pasado,
            fecha__year=año_pasado
        ).count()
        
        # USUARIOS
        from django.contrib.auth.models import User
        total_usuarios = User.objects.count()
        admins = User.objects.filter(is_staff=True).count()
        
        # CITAS POR DÍA (Últimos 7 días)
        citas_por_dia = []
        for i in range(7, 0, -1):
            fecha = (datetime.now() - timedelta(days=i)).date()
            count = Cita.objects.filter(fecha=fecha).count()
            citas_por_dia.append({
                'fecha': fecha.strftime('%d/%m'),
                'count': count
            })
        
        # Duración promedio de atención
        duraciones = Cita.objects.filter(
            duracion_atencion_minutos__isnull=False
        ).values_list('duracion_atencion_minutos', flat=True)
        
        duracion_promedio = sum(duraciones) / len(duraciones) if duraciones else 0
        
        data = {
            'pacientes': {
                'total': total_pacientes,
                'activos': pacientes_activos,
                'con_seguro': pacientes_con_seguro,
                'sin_seguro': pacientes_sin_seguro,
                'por_genero': pacientes_por_genero,
            },
            'citas': {
                'total': total_citas,
                'hoy': citas_hoy,
                'programadas': citas_programadas,
                'canceladas': citas_canceladas,
                'completadas': citas_completadas,
                'este_mes': citas_este_mes,
                'mes_pasado': citas_mes_pasado,
                'por_estado': citas_por_estado,
                'por_tipo': citas_por_tipo,
                'por_especialidad': citas_por_especialidad,
                'por_medico': citas_por_medico,
                'por_dia': citas_por_dia,
                'duracion_promedio': round(duracion_promedio, 1),
            },
            'ecografias': {
                'total': total_ecografias,
                'completadas': ecografias_realizadas,
                'pendientes': ecografias_pendientes,
            },
            'medicos': {
                'total': total_medicos,
                'activos': medicos_con_turnos,
            },
            'especialidades': {
                'total': total_especialidades,
            },
            'contratos': {
                'total': total_contratos,
                'vigentes': contratos_vigentes,
            },
            'usuarios': {
                'total': total_usuarios,
                'admins': admins,
            }
        }
        
        return JsonResponse(data)
    
    except Exception as e:
        error_msg = f"Error en dashboard API: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        print(error_msg)
        
        # Retornar error con detalles
        return JsonResponse({
            'error': str(e),
            'type': type(e).__name__,
            'detail': traceback.format_exc() if settings.DEBUG else 'Error interno'
        }, status=500)


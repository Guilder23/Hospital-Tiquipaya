from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta, date
import uuid

# Importacioines para generar PDF
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO

from apps.citas_ecografia.models import CitaEcografia
from apps.citas.models import Cita
from apps.pacientes.models import Paciente
from apps.especialidades.models import Especialidad
from apps.accounts.models import Medico, Ecografo
from apps.horarios.models import DiasAtencion
from apps.permisos.utils import es_admin_o_staff


def _tiene_permiso_edicion(request):
    """Verifica si el usuario tiene permisos para editar/crear citas"""
    if es_admin_o_staff(request.user):
        return True
    permiso = getattr(request, 'permiso_actual', None)
    return permiso and permiso.puede_editar()


def _obtener_nombre_dia(fecha):
    """Obtiene el nombre del día de la semana (0=lunes, 6=domingo)"""
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    return dias[fecha.weekday()]


def _medico_trabaja_en_dia(medico, fecha):
    """Verifica si un médico trabaja en un día específico"""
    if not medico.dias_atencion:
        return True
    
    nombre_dia = _obtener_nombre_dia(fecha)
    dias_atencion = medico.dias_atencion
    
    atributos_dia = {
        'lunes': 'lunes',
        'martes': 'martes',
        'miercoles': 'miercoles',
        'jueves': 'jueves',
        'viernes': 'viernes',
        'sabado': 'sabado',
        'domingo': 'domingo'
    }
    
    atributo = atributos_dia.get(nombre_dia)
    if atributo:
        return getattr(dias_atencion, atributo, False)
    return False


def _slots_turno(turno_obj, fecha):
    """Genera slots de 30 minutos basado en un objeto Turno"""
    slots = []
    if not turno_obj:
        return slots
    
    try:
        inicio = turno_obj.hora_ini
        fin = turno_obj.hora_fin
    except AttributeError:
        return slots
    
    from datetime import datetime as dt
    h = dt.combine(fecha, inicio)
    limite = dt.combine(fecha, fin)
    
    while h < limite:
        slots.append(h.time())
        h += timedelta(minutes=30)
    
    return slots


@login_required
@login_required
def citas_ecografia_list(request):
    """Lista todas las citas de ecografía del Personal de Admisión"""
    # Verificar permisos: superusuario o permiso asignado
    if not (es_admin_o_staff(request.user) or getattr(request, 'permiso_actual', None)):
        messages.error(request, 'No tienes acceso a esta sección')
        return redirect('home')
    
    permiso = getattr(request, 'permiso_actual', None)
    citas = CitaEcografia.objects.all().select_related('paciente', 'especialidad', 'medico')
    especialidades = Especialidad.objects.filter(estado=True)
    ecografos = Ecografo.objects.all().select_related('user__perfil')
    ctx = {
        'citas': citas,
        'especialidades': especialidades,
        'ecografos': ecografos,
        'permiso_actual': permiso,
    }
    return render(request, 'citas_ecografia/citas_ecografia.html', ctx)

# vista para eu el ecografo vea sus citas agendadas
@login_required
def mis_citas_ecografia(request):
    """Vista para que el ecógrafo vea sus citas de ecografía agendadas"""
    # Verificar que el usuario sea ecógrafo
    try:
        ecografo = request.user.ecografo
    except Exception:
        messages.error(request, 'No tienes acceso a esta sección. Solo ecógrafos pueden acceder.')
        return redirect('home')
    
    # Obtener todas las citas agendadas para este ecógrafo
    # Ordenadas por fecha y hora
    citas = CitaEcografia.objects.filter(
        medico=ecografo
    ).exclude(
        estado='CANCELADA'
    ).select_related(
        'paciente', 'especialidad', 'medico'
    ).order_by('fecha', 'hora')
    
    # Separar citas por estado y fecha
    citas_hoy = []
    citas_proximas = []
    citas_atendidas = []
    
    hoy = timezone.now().date()
    
    for cita in citas:
        # Si la cita está REALIZADA, va al historial
        if cita.estado == 'REALIZADA':
            citas_atendidas.append(cita)
        # Si es de hoy y no está realizada
        elif cita.fecha == hoy:
            citas_hoy.append(cita)
        # Si es futura
        elif cita.fecha > hoy:
            citas_proximas.append(cita)
        # Si es pasada pero no fue atendida, va a próximas (no mostrar en atendidas)
        # Las citas pasadas no atendidas no se mostrarán en ninguna sección
    
    # Ordenar atendidas por fecha descendente (más recientes primero)
    citas_atendidas.sort(key=lambda x: (x.fecha, x.hora), reverse=True)
    
    ctx = {
        'citas_hoy': citas_hoy,
        'citas_proximas': citas_proximas,
        'citas_atendidas': citas_atendidas,
        'total_citas': len(citas),
        'total_atendidas': len([c for c in citas_atendidas if c.estado == 'REALIZADA']),
        'ecografo': ecografo,
    }
    return render(request, 'citas_ecografia/mis_citas.html', ctx)


@login_required
def pacientes_atendidos_ecografia(request):
    """Vista para mostrar historial de pacientes atendidos en tabla"""
    try:
        ecografo = request.user.ecografo
    except Exception:
        messages.error(request, 'No tienes acceso a esta sección.')
        return redirect('home')
    
    # Filtros
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    buscar = request.GET.get('buscar', '')
    
    # Base query - solo citas realizadas
    citas = CitaEcografia.objects.filter(
        medico=ecografo,
        estado='REALIZADA'
    ).select_related(
        'paciente', 'especialidad'
    ).order_by('-fecha', '-hora')
    
    # Aplicar filtros
    if fecha_desde:
        citas = citas.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        citas = citas.filter(fecha__lte=fecha_hasta)
    if buscar:
        citas = citas.filter(
            Q(paciente__nombres__icontains=buscar) |
            Q(paciente__apellido_paterno__icontains=buscar) |
            Q(paciente__ci__icontains=buscar)
        )
    
    # Estadísticas
    hoy = timezone.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    
    atendidos_hoy = CitaEcografia.objects.filter(
        medico=ecografo,
        estado='REALIZADA',
        fecha=hoy
    ).count()
    
    atendidos_semana = CitaEcografia.objects.filter(
        medico=ecografo,
        estado='REALIZADA',
        fecha__gte=inicio_semana
    ).count()
    
    ctx = {
        'citas_atendidas': citas,
        'atendidos_hoy': atendidos_hoy,
        'atendidos_semana': atendidos_semana,
        'filtro_desde': fecha_desde,
        'filtro_hasta': fecha_hasta,
        'filtro_buscar': buscar,
        'ecografo': ecografo,
    }
    return render(request, 'citas_ecografia/pacientes_atendidos.html', ctx)


@login_required
@require_POST
def atender_cita_ecografia(request, cita_id):
    """Marcar una cita como en atención y registrar el inicio"""
    try:
        ecografo = request.user.ecografo
    except Exception:
        return JsonResponse({
            'ok': False,
            'error': 'No tienes permiso para acceder a esta funcionalidad'
        }, status=403)
    
    try:
        cita = CitaEcografia.objects.get(id=cita_id, medico=ecografo)
        
        # Cambiar estado a EN_ATENCION
        cita.estado_atencion = 'EN_ATENCION'
        cita.tiempo_inicio_atencion = timezone.now()
        cita.save()
        
        return JsonResponse({
            'ok': True,
            'mensaje': 'Cita marcada como "En Atención"',
            'cita_id': cita.id
        })
    
    except CitaEcografia.DoesNotExist:
        return JsonResponse({
            'ok': False,
            'error': 'Cita no encontrada o no pertenece a ti'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'error': str(e)
        }, status=500)


@login_required
def ver_detalle_cita_ecografia(request, cita_id):
    """Ver detalles completos de una cita de ecografía"""
    try:
        ecografo = request.user.ecografo
    except Exception:
        messages.error(request, 'No tienes permiso para acceder')
        return redirect('home')
    
    try:
        cita = CitaEcografia.objects.get(id=cita_id, medico=ecografo)
    except CitaEcografia.DoesNotExist:
        messages.error(request, 'Cita no encontrada')
        return redirect('citas_ecografia:mis_citas')
    
    from datetime import date
    es_hoy = cita.fecha == date.today()
    
    ctx = {
        'cita': cita,
        'ecografo': ecografo,
        'es_hoy': es_hoy,
    }
    return render(request, 'citas_ecografia/detalle_cita.html', ctx)


@login_required
@require_POST
def guardar_resultado_cita(request, cita_id):
    """Guardar resultado de la ecografía y marcar como realizada"""
    try:
        ecografo = request.user.ecografo
    except Exception:
        return JsonResponse({
            'ok': False,
            'error': 'No tienes permiso'
        }, status=403)
    
    try:
        cita = CitaEcografia.objects.get(id=cita_id, medico=ecografo)
        
        resultado = request.POST.get('resultado_ecografia', '')
        
        # Actualizar resultado y estado
        cita.resultado_ecografia = resultado
        cita.estado = 'REALIZADA'
        cita.estado_atencion = 'ATENDIDO'
        cita.tiempo_fin_atencion = timezone.now()
        cita.save()
        
        return JsonResponse({
            'ok': True,
            'mensaje': 'Resultado guardado. Cita marcada como realizada'
        })
    
    except CitaEcografia.DoesNotExist:
        return JsonResponse({
            'ok': False,
            'error': 'Cita no encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'error': str(e)
        }, status=500)


@login_required
def agendar_cita_ecografia(request):
    """Vista para agendar nueva cita de ecografía"""
    if not _tiene_permiso_edicion(request):
        messages.error(request, 'No tienes acceso a esta sección')
        return redirect('home')
    
    paciente = None
    especialidad = None
    comentario_medico = None
    medicos_disponibles = []
    
    if request.method == 'POST':
        ci = request.POST.get('ci')
        nombre = request.POST.get('nombre')
        
        # Buscar paciente
        if ci:
            try:
                paciente = Paciente.objects.get(ci=ci)
            except Paciente.DoesNotExist:
                messages.error(request, 'Paciente no encontrado')
        elif nombre:
            pacientes = Paciente.objects.filter(
                Q(nombres__icontains=nombre) | 
                Q(apellido_paterno__icontains=nombre)
            )
            if pacientes.count() == 1:
                paciente = pacientes.first()
            elif pacientes.count() > 1:
                messages.warning(request, 'Se encontraron múltiples pacientes con ese nombre')
            else:
                messages.error(request, 'Paciente no encontrado')
        
        if paciente:
            # Verificar si el paciente está habilitado para ecografía
            cita_consulta = Cita.objects.filter(
                paciente=paciente,
                requiere_ecografia=True
            ).first()
            
            if not cita_consulta:
                messages.warning(request, 'Este paciente no está habilitado para ecografía')
            else:
                especialidad = cita_consulta.ecografia.especialidad if cita_consulta.ecografia else None
                comentario_medico = cita_consulta.comentario_ecografia
                
                # Obtener ecógrafos asignados a esta ecografía específica
                if cita_consulta.ecografia:
                    ecografos = cita_consulta.ecografia.ecografos.all()
                    # Si no hay ecógrafos asignados a esta ecografía, buscar ecógrafos de esa especialidad
                    if not ecografos.exists():
                        ecografos = Ecografo.objects.filter(
                            ecografias_asignadas__especialidad=cita_consulta.ecografia.especialidad
                        ).distinct()
                    medicos_disponibles = ecografos
    
    ctx = {
        'paciente': paciente,
        'especialidad': especialidad,
        'comentario_medico': comentario_medico,
        'medicos_disponibles': medicos_disponibles,
    }
    return render(request, 'citas_ecografia/agendar.html', ctx)


@login_required
@require_POST
def buscar_paciente_ecografia(request):
    """API para buscar paciente por CI y obtener TODAS las ecografías habilitadas pendientes"""
    import json
    try:
        data = json.loads(request.body)
        term = data.get('search', '').strip()
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Formato de datos inválido'}, status=400)

    if not term or not term.isdigit():
        return JsonResponse({'ok': False, 'error': 'Debes ingresar el CI del paciente'}, status=400)

    try:
        paciente = Paciente.objects.get(ci=term)
    except Paciente.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Paciente no encontrado'}, status=404)

    # Obtener TODAS las citas con ecografía habilitada para este paciente
    citas_con_ecografia = Cita.objects.filter(
        paciente=paciente,
        requiere_ecografia=True,
        ecografia__isnull=False
    ).select_related('ecografia', 'ecografia__especialidad', 'medico__user__perfil')

    # Obtener IDs de citas que YA tienen una CitaEcografia programada o realizada
    citas_ya_agendadas = CitaEcografia.objects.filter(
        paciente=paciente,
        cita_consulta__isnull=False,
        estado__in=['PROGRAMADA', 'REALIZADA', 'REPROGRAMADA']
    ).values_list('cita_consulta_id', flat=True)

    # Filtrar las citas que aún no tienen cita de ecografía agendada
    ecografias_disponibles = []
    for cita in citas_con_ecografia:
        # Si esta cita ya tiene una cita de ecografía agendada, no mostrarla
        if cita.id in citas_ya_agendadas:
            continue
        
        # Obtener ecógrafos disponibles para esta ecografía
        ecografos = []
        if cita.ecografia:
            ecografos_qs = cita.ecografia.ecografos.all()
            if not ecografos_qs.exists():
                ecografos_qs = Ecografo.objects.filter(
                    ecografias__especialidad=cita.ecografia.especialidad
                ).distinct()
            
            ecografos = [
                {'id': e.id, 'nombre': f"{e.user.perfil.nombres} {e.user.perfil.apellido_paterno}"}
                for e in ecografos_qs
            ]
        
        # Obtener nombre del médico que solicitó la ecografía
        medico_solicitante = ''
        if cita.medico and hasattr(cita.medico, 'user') and hasattr(cita.medico.user, 'perfil'):
            perfil = cita.medico.user.perfil
            medico_solicitante = f"{perfil.nombres} {perfil.apellido_paterno}"
        
        ecografias_disponibles.append({
            'cita_id': cita.id,
            'especialidad_id': cita.ecografia.especialidad.id if cita.ecografia else None,
            'especialidad_nombre': cita.ecografia.especialidad.nombre if cita.ecografia else None,
            'ecografia_id': cita.ecografia.id if cita.ecografia else None,
            'ecografia_nombre': cita.ecografia.nombre if cita.ecografia else None,
            'comentario_medico': cita.comentario_ecografia or '',
            'medico_solicitante': medico_solicitante,
            'fecha_solicitud': cita.fecha.strftime('%d/%m/%Y') if cita.fecha else '',
            'ecografos_disponibles': ecografos
        })

    return JsonResponse({
        'ok': True,
        'paciente': {
            'id': paciente.id,
            'nombres': paciente.nombres,
            'apellido_paterno': paciente.apellido_paterno,
            'ci': paciente.ci,
            'edad': paciente.get_edad() if paciente.get_edad() else 'N/A'
        },
        'habilitado': len(ecografias_disponibles) > 0,
        'ecografias_disponibles': ecografias_disponibles,
        'total_ecografias': len(ecografias_disponibles)
    })


@login_required
@require_POST
def obtener_horarios_medico(request):
    """API para obtener horarios disponibles de un médico para una fecha"""
    medico_id = request.POST.get('medico_id')
    fecha_str = request.POST.get('fecha')
    
    if not medico_id or not fecha_str:
        return JsonResponse({
            'ok': False,
            'error': 'Médico y fecha son requeridos'
        }, status=400)
    
    try:
        medico = Medico.objects.get(id=medico_id)
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except (Medico.DoesNotExist, ValueError):
        return JsonResponse({
            'ok': False,
            'error': 'Médico o fecha inválidos'
        }, status=400)
    
    # Verificar que el médico trabaja ese día
    nombre_dia = _obtener_nombre_dia(fecha)
    if not _medico_trabaja_en_dia(medico, fecha):
        return JsonResponse({
            'ok': False,
            'error': f'El médico no trabaja el {nombre_dia}'
        }, status=400)
    else:
        mensaje_trabaja = f'El médico trabaja el {nombre_dia}'
    
    # Obtener turnos del médico
    turnos = medico.turnos.filter(estado=True).order_by('hora_ini')
    
    horarios = {}
    citas_ocupadas = set(
        CitaEcografia.objects.filter(
            medico=medico,
            fecha=fecha
        ).exclude(
            estado='CANCELADA'
        ).values_list('hora', flat=True)
    )
    
    for turno in turnos:
        slots = _slots_turno(turno, fecha)
        horarios[turno.nombre] = [
            {
                'hora': h.strftime('%H:%M'),
                'disponible': h not in citas_ocupadas
            }
            for h in slots
        ]
    
    return JsonResponse({
        'ok': True,
        'horarios': horarios,
        'mensaje': mensaje_trabaja
    })


@login_required
@require_POST
def obtener_horarios_ecografo(request):
    """API para obtener horarios disponibles de un ecógrafo para una fecha específica"""
    ecografo_id = request.POST.get('ecografo_id')
    fecha_str = request.POST.get('fecha')
    
    if not ecografo_id or not fecha_str:
        return JsonResponse({
            'ok': False,
            'error': 'Ecógrafo y fecha son requeridos'
        }, status=400)
    
    try:
        ecografo = Ecografo.objects.get(id=ecografo_id)
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except (Ecografo.DoesNotExist, ValueError):
        return JsonResponse({
            'ok': False,
            'error': 'Ecógrafo o fecha inválidos'
        }, status=400)
    
    # Obtener turnos del ecógrafo
    turnos = ecografo.turnos.filter(estado=True).order_by('hora_ini')
    
    # Obtener horas ocupadas
    citas_ocupadas = set(
        CitaEcografia.objects.filter(
            medico=ecografo,
            fecha=fecha
        ).exclude(
            estado='CANCELADA'
        ).values_list('hora', flat=True)
    )
    
    horarios_disponibles = []
    horarios_ocupados = []
    total_slots = 0
    slots_ocupados = 0
    
    for turno in turnos:
        slots = _slots_turno(turno, fecha)
        total_slots += len(slots)
        
        for slot in slots:
            hora_str = slot.strftime('%H:%M')
            if slot in citas_ocupadas:
                horarios_ocupados.append(hora_str)
                slots_ocupados += 1
            else:
                horarios_disponibles.append(hora_str)
    
    # Determinar si el día está completamente ocupado
    dia_completamente_ocupado = total_slots > 0 and slots_ocupados == total_slots
    
    return JsonResponse({
        'ok': True,
        'fecha': fecha_str,
        'horarios_disponibles': horarios_disponibles,
        'horarios_ocupados': horarios_ocupados,
        'total_slots': total_slots,
        'slots_ocupados': slots_ocupados,
        'dia_completamente_ocupado': dia_completamente_ocupado
    })


@login_required
def verificar_dias_ocupados_ecografo(request, ecografo_id):
    """API para verificar qué días están completamente ocupados para un ecógrafo"""
    try:
        ecografo = Ecografo.objects.get(id=ecografo_id)
    except Ecografo.DoesNotExist:
        return JsonResponse({
            'ok': False,
            'error': 'Ecógrafo no encontrado'
        }, status=404)
    
    # Obtener rango de fechas (próximos 60 días)
    fecha_inicio = date.today()
    fecha_fin = fecha_inicio + timedelta(days=60)
    
    dias_ocupados = []
    
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        # Verificar si el ecógrafo trabaja este día
        if _medico_trabaja_en_dia(ecografo, fecha_actual):
            # Obtener turnos y slots del día
            turnos = ecografo.turnos.filter(estado=True)
            total_slots = 0
            
            for turno in turnos:
                slots = _slots_turno(turno, fecha_actual)
                total_slots += len(slots)
            
            # Contar citas ocupadas
            citas_ocupadas = CitaEcografia.objects.filter(
                medico=ecografo,
                fecha=fecha_actual
            ).exclude(
                estado='CANCELADA'
            ).count()
            
            # Si está completamente ocupado
            if total_slots > 0 and citas_ocupadas >= total_slots:
                dias_ocupados.append(fecha_actual.strftime('%Y-%m-%d'))
        
        fecha_actual += timedelta(days=1)
    
    return JsonResponse({
        'ok': True,
        'dias_ocupados': dias_ocupados
    })


@login_required
@require_POST
def crear_cita_ecografia(request):
    """Crear nueva cita de ecografía"""
    if not _tiene_permiso_edicion(request):
        return JsonResponse({
            'ok': False,
            'error': 'No tienes acceso'
        }, status=403)
    
    try:
        paciente_id = request.POST.get('paciente_id')
        ecografo_id = request.POST.get('ecografo_id')
        fecha_str = request.POST.get('fecha')
        hora_str = request.POST.get('hora')
        cita_consulta_id = request.POST.get('cita_consulta_id')
        
        paciente = Paciente.objects.get(id=paciente_id)
        ecografo = Ecografo.objects.get(id=ecografo_id)
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()
        
        # Obtener la cita de consulta específica que se seleccionó
        if cita_consulta_id:
            cita_consulta = Cita.objects.get(id=cita_consulta_id, paciente=paciente)
        else:
            # Fallback: buscar primera cita con ecografía habilitada (compatibilidad)
            cita_consulta = Cita.objects.filter(
                paciente=paciente,
                requiere_ecografia=True
            ).first()
        
        if not cita_consulta:
            return JsonResponse({
                'ok': False,
                'error': 'Paciente no está habilitado para ecografía'
            }, status=400)
        
        # Verificar que esta cita no tenga ya una cita de ecografía agendada
        cita_existente = CitaEcografia.objects.filter(
            cita_consulta=cita_consulta,
            estado__in=['PROGRAMADA', 'REALIZADA', 'REPROGRAMADA']
        ).exists()
        
        if cita_existente:
            return JsonResponse({
                'ok': False,
                'error': 'Esta ecografía ya tiene una cita agendada'
            }, status=400)
        
        # Generar código único
        codigo = f"ECO{uuid.uuid4().hex[:8].upper()}"
        
        cita = CitaEcografia.objects.create(
            paciente=paciente,
            medico=ecografo,
            especialidad=cita_consulta.ecografia.especialidad,
            fecha=fecha,
            hora=hora,
            codigo=codigo,
            comentario_medico=cita_consulta.comentario_ecografia,
            cita_consulta=cita_consulta
        )
        
        msg = f'Cita de ecografía agendada correctamente para {paciente.nombres}'
        messages.success(request, msg)
        
        return JsonResponse({
            'ok': True,
            'mensaje': 'Cita de ecografía creada exitosamente',
            'cita_id': cita.id
        })
    
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'error': str(e)
        }, status=500)


@login_required
@require_POST
def editar_cita_ecografia(request, cita_id):
    """Editar cita de ecografía"""
    if not _tiene_permiso_edicion(request):
        return JsonResponse({
            'ok': False,
            'error': 'No tienes acceso'
        }, status=403)
    
    try:
        cita = CitaEcografia.objects.get(id=cita_id)
        
        # Actualizar campos
        fecha_str = request.POST.get('fecha')
        hora_str = request.POST.get('hora')
        estado = request.POST.get('estado')
        comentario_medico = request.POST.get('comentario_medico', '')
        resultado_ecografia = request.POST.get('resultado_ecografia', '')
        
        if fecha_str:
            cita.fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        if hora_str:
            cita.hora = datetime.strptime(hora_str, '%H:%M').time()
        if estado:
            cita.estado = estado
        
        cita.comentario_medico = comentario_medico
        cita.resultado_ecografia = resultado_ecografia
        cita.save()
        
        msg = 'Cita de ecografía actualizada correctamente'
        messages.success(request, msg)
        
        return JsonResponse({
            'ok': True,
            'mensaje': 'Cita actualizada exitosamente'
        })
    
    except CitaEcografia.DoesNotExist:
        return JsonResponse({
            'ok': False,
            'error': 'Cita no encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'error': str(e)
        }, status=500)


@login_required
@require_POST
def cancelar_cita_ecografia(request, cita_id):
    """Cancelar cita de ecografía"""
    if not _tiene_permiso_edicion(request):
        return JsonResponse({
            'ok': False,
            'error': 'No tienes acceso'
        }, status=403)
    
    try:
        cita = CitaEcografia.objects.get(id=cita_id)
        cita.estado = 'CANCELADA'
        cita.save()
        
        return JsonResponse({
            'ok': True,
            'mensaje': 'Cita cancelada exitosamente'
        })
    except CitaEcografia.DoesNotExist:
        return JsonResponse({
            'ok': False,
            'error': 'Cita no encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'error': str(e)
        }, status=500)

# generar_pdf  de cita para ecografia
def generar_pdf_cita(request, cita_id):
    """Genera un comprobante PDF profesional para la cita de ecografía"""
    cita = get_object_or_404(CitaEcografia, id=cita_id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.4*inch,
        bottomMargin=0.4*inch,
        leftMargin=0.4*inch,
        rightMargin=0.4*inch
    )

    elementos = []
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        'TituloHospital',
        parent=styles['Heading1'],
        fontSize=17,
        textColor=colors.HexColor('#1e5a7d'),
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )

    subtitulo_style = ParagraphStyle(
        'Subtitulo',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#34495e'),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    seccion_style = ParagraphStyle(
        'Seccion',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )

    elementos.append(Paragraph('<b>HOSPITAL TIQUIPAYA</b>', titulo_style))
    elementos.append(Paragraph('Comprobante de Cita - Servicio de Ecografía', subtitulo_style))

    line_table = Table([['']], colWidths=[7.2*inch])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1e5a7d')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(line_table)

    elementos.append(Paragraph('<b>INFORMACIÓN DE LA CITA</b>', seccion_style))

    datos_principales = [
        ['Número de Cita:', f'EC-{cita.id:06d}'],
        ['Fecha de Emisión:', date.today().strftime('%d/%m/%Y')],
        ['Estado:', cita.estado],
    ]

    tabla_principales = Table(datos_principales, colWidths=[2.4*inch, 4.6*inch])
    tabla_principales.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla_principales)
    elementos.append(Spacer(1, 0.1*inch))

    elementos.append(Paragraph('<b>DATOS DEL PACIENTE</b>', seccion_style))

    datos_paciente = [
        ['Nombre Completo:', f'{cita.paciente.nombres} {cita.paciente.apellido_paterno} {cita.paciente.apellido_materno}'],
        ['CI:', cita.paciente.ci or 'No registrado'],
        ['Fecha de Nacimiento:', cita.paciente.fecha_nacimiento.strftime('%d/%m/%Y') if cita.paciente.fecha_nacimiento else 'No registrada'],
        ['Teléfono:', cita.paciente.celular or 'No registrado'],
    ]

    tabla_paciente = Table(datos_paciente, colWidths=[2.4*inch, 4.6*inch])
    tabla_paciente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#a5d6a7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla_paciente)
    elementos.append(Spacer(1, 0.1*inch))

    elementos.append(Paragraph('<b>DETALLES DE LA CITA</b>', seccion_style))

    datos_medicos = [
        ['Especialidad:', cita.especialidad.nombre],
        ['Ecógrafo:', f'{cita.medico.user.perfil.nombres} {cita.medico.user.perfil.apellido_paterno}'],
        ['Consultorio:', cita.medico.consultorio or 'No asignado'],
        ['Fecha de Cita:', cita.fecha.strftime('%d/%m/%Y')],
        ['Hora de Cita:', cita.hora.strftime('%H:%M')],
    ]

    tabla_medica = Table(datos_medicos, colWidths=[2.4*inch, 4.6*inch])
    tabla_medica.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#90caf9')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla_medica)
    elementos.append(Spacer(1, 0.1*inch))

    if cita.cita_consulta and cita.cita_consulta.medico:
        elementos.append(Paragraph('<b>INFORMACIÓN ADICIONAL</b>', seccion_style))

        medico_solicitante = cita.cita_consulta.medico
        datos_adicionales = [
            ['Médico Solicitante:', f'Dr(a). {medico_solicitante.user.perfil.nombres} {medico_solicitante.user.perfil.apellido_paterno}']
        ]

        if cita.comentario_medico:
            datos_adicionales.append(['Comentario Médico:', cita.comentario_medico])

        tabla_adicional = Table(datos_adicionales, colWidths=[2.4*inch, 4.6*inch])
        tabla_adicional.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff9c4')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fff59d')),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elementos.append(tabla_adicional)
        elementos.append(Spacer(1, 0.1*inch))

    instrucciones_style = ParagraphStyle(
        'Instrucciones',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#e74c3c'),
        leftIndent=10,
        rightIndent=10,
        spaceBefore=6,
        spaceAfter=6
    )

    instrucciones = Paragraph(
        '<b>INSTRUCCIONES IMPORTANTES:</b><br/>'
        '• Presentarse 15 minutos antes de la hora programada<br/>'
        '• Traer carnet de identidad original<br/>'
        '• Si tiene seguro médico, traer la documentación correspondiente<br/>'
        '• En caso de no poder asistir, cancelar con 24 horas de anticipación',
        instrucciones_style
    )
    elementos.append(instrucciones)

    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER,
        spaceBefore=10
    )

    footer = Paragraph(
        'Hospital Tiquipaya - Servicio de Ecografía<br/>'
        'Este documento es un comprobante de cita médica<br/>'
        f'Generado el {date.today().strftime("%d/%m/%Y")}',
        footer_style
    )
    elementos.append(footer)

    doc.build(elementos)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cita_ecografia_{cita.id}_{cita.paciente.ci}.pdf"'
    response.write(pdf)

    return response

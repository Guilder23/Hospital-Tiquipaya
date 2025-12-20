from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import uuid

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
    ctx = {
        'citas': citas,
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
        # Si es pasada pero no fue atendida
        else:
            citas_atendidas.append(cita)
    
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
    
    ctx = {
        'cita': cita,
        'ecografo': ecografo,
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
    """API para buscar paciente por CI o nombre"""
    import json
    try:
        data = json.loads(request.body)
        term = data.get('search', '').strip()
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Formato de datos inválido'}, status=400)

    paciente = None
    habilitado = False
    especialidad_id = None
    especialidad_nombre = None
    comentario_medico = None
    medicos_disponibles = []
    ecografia_asignada = None

    if not term or not term.isdigit():
        return JsonResponse({'ok': False, 'error': 'Debes ingresar el CI del paciente'}, status=400)

    try:
        paciente = Paciente.objects.get(ci=term)
    except Paciente.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Paciente no encontrado'}, status=404)

    cita_consulta = Cita.objects.filter(
        paciente=paciente,
        requiere_ecografia=True
    ).first()

    if cita_consulta:
        habilitado = True
        especialidad_id = cita_consulta.ecografia.especialidad.id if cita_consulta.ecografia else None
        especialidad_nombre = cita_consulta.ecografia.especialidad.nombre if cita_consulta.ecografia else None
        comentario_medico = cita_consulta.comentario_ecografia
        ecografia_asignada = cita_consulta.ecografia.nombre if cita_consulta.ecografia else None
        
        # Obtener ecógrafos que tienen asignada esta ecografía específica
        if cita_consulta.ecografia:
            ecografos = cita_consulta.ecografia.ecografos.all()
            # Si no hay ecógrafos asignados a esta ecografía, buscar ecógrafos de esa especialidad
            if not ecografos.exists():
                ecografos = Ecografo.objects.filter(
                    ecografias__especialidad=cita_consulta.ecografia.especialidad
                ).distinct()
            
            medicos_disponibles = [
                {'id': e.id, 'nombre': f"{e.user.perfil.nombres} {e.user.perfil.apellido_paterno}"}
                for e in ecografos
            ]

    return JsonResponse({
        'ok': True,
        'paciente': {
            'id': paciente.id,
            'nombres': paciente.nombres,
            'apellido_paterno': paciente.apellido_paterno,
            'ci': paciente.ci,
            'edad': paciente.get_edad() if paciente.get_edad() else 'N/A'
        },
        'habilitado': habilitado,
        'especialidad_id': especialidad_id,
        'especialidad_nombre': especialidad_nombre,
        'comentario_medico': comentario_medico,
        'ecografia_asignada': ecografia_asignada,
        'medicos_disponibles': medicos_disponibles
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
        
        paciente = Paciente.objects.get(id=paciente_id)
        ecografo = Ecografo.objects.get(id=ecografo_id)
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()
        
        # Obtener cita consulta para especialidad y comentario
        cita_consulta = Cita.objects.filter(
            paciente=paciente,
            requiere_ecografia=True
        ).first()
        
        if not cita_consulta:
            return JsonResponse({
                'ok': False,
                'error': 'Paciente no está habilitado para ecografía'
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

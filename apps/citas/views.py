from datetime import datetime, timedelta, time
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.pacientes.models import Paciente
from apps.accounts.models import Medico
from apps.citas.models import Cita
from apps.ecografias.models import Ecografia
from apps.horarios.models import Turnos
from django.db import IntegrityError

def _manana():
    hoy = datetime.now().date()
    return hoy + timedelta(days=1)

def _generar_codigo_unico(tipo=''):
    """Genera un código único verificando en la base de datos"""
    max_intentos = 10
    for _ in range(max_intentos):
        codigo = f"{tipo}{uuid.uuid4().hex[:8].upper()}"
        if not Cita.objects.filter(codigo=codigo).exists():
            return codigo
    # Si después de 10 intentos no genera uno único, usar timestamp
    timestamp = int(timezone.now().timestamp() * 1000) % 1000000
    return f"{tipo}{timestamp:08d}"

def _slots_turno(turno_obj):
    """Genera slots de 30 minutos basado en un objeto Turno
    
    Args:
        turno_obj: Objeto Turnos con hora_ini y hora_fin
    
    Returns:
        Lista de objetos time con intervalos de 30 minutos
    """
    slots = []
    if not turno_obj:
        return slots
    
    try:
        inicio = turno_obj.hora_ini
        fin = turno_obj.hora_fin
    except AttributeError:
        return slots
    
    h = datetime.combine(_manana(), inicio)
    limite = datetime.combine(_manana(), fin)
    
    while h < limite:
        slots.append(h.time())
        h += timedelta(minutes=30)
    
    return slots

@require_POST
def validar_paciente(request):
    ci = request.POST.get('ci', '').strip()
    fn = request.POST.get('fecha_nacimiento', '').strip()
    try:
        fecha_nac = datetime.strptime(fn, '%Y-%m-%d').date()
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Fecha inválida'}, status=400)
    try:
        p = Paciente.objects.get(ci=ci, fecha_nacimiento=fecha_nac, activo=True)
    except Paciente.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Paciente no encontrado, Verifica tus datos y si no estas registrado registrate con el personal de Admision en el Hospital Tiquipaya'}, status=404)
    request.session['paciente_id'] = p.id
    return JsonResponse({'ok': True, 'redirect': reverse('citas:agendar')})

@ensure_csrf_cookie
def agendar_inicio(request):
    pid = request.session.get('paciente_id')
    manana = _manana()
    
    # Obtener todos los turnos activos
    turnos_activos = Turnos.objects.filter(estado=True).order_by('hora_ini')
    
    # Para cada turno, obtener los médicos que trabajan en ese turno
    turnos_data = []
    for turno in turnos_activos:
        medicos = Medico.objects.filter(turnos=turno)
        turnos_data.append({
            'turno': turno,
            'medicos': medicos
        })
    
    ctx = {
        'paciente_validado': bool(pid),
        'fecha_objetivo': manana,
        'turnos_data': turnos_data,
    }
    return render(request, 'citas/agendar.html', ctx)

def agenda_medico(request, medico_id):
    m = get_object_or_404(Medico, id=medico_id)
    manana = _manana()
    
    # Obtener los turnos del médico
    turnos_medico = m.turnos.filter(estado=True).order_by('hora_ini')
    
    resultado = {}
    ocupados = set(Cita.objects.filter(medico=m, fecha=manana).exclude(estado='CANCELADA').values_list('hora', flat=True))
    
    for turno in turnos_medico:
        lista = []
        for h in _slots_turno(turno):
            lista.append({
                'hora': h.strftime('%H:%M'),
                'ocupado': h in ocupados
            })
        resultado[turno.nombre] = lista
    
    return JsonResponse({'fecha': manana.strftime('%Y-%m-%d'), 'turnos': resultado})

@require_POST
def confirmar_cita(request):
    pid = request.session.get('paciente_id')
    if not pid:
        return JsonResponse({'ok': False, 'error': 'Paciente no validado'}, status=403)
    medico_id = request.POST.get('medico_id')
    hora_str = request.POST.get('hora')
    m = get_object_or_404(Medico, id=medico_id)
    manana = _manana()
    try:
        h = datetime.strptime(hora_str, '%H:%M').time()
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Hora inválida'}, status=400)
    if Cita.objects.filter(paciente_id=pid, fecha=manana).exclude(estado='CANCELADA').exists():
        return JsonResponse({'ok': False, 'error': 'Solo puedes tener una cita. Si quieres cambiar de horario primero debes cancelarla y escoger un nuevo horario'}, status=409)
    
    # Validar que la hora está dentro de los turnos del médico
    turno_ok = False
    for turno in m.turnos.filter(estado=True):
        if turno.hora_ini <= h < turno.hora_fin:
            turno_ok = True
            break
    
    if not turno_ok:
        return JsonResponse({'ok': False, 'error': 'Hora fuera de turno'}, status=400)
    
    if Cita.objects.filter(medico=m, fecha=manana, hora=h).exclude(estado='CANCELADA').exists():
        return JsonResponse({'ok': False, 'error': 'Slot ocupado'}, status=409)
    paciente = get_object_or_404(Paciente, id=pid)
    codigo = uuid.uuid4().hex[:10].upper()
    # Eliminar registros cancelados del mismo slot para liberar la restricción si existe
    Cita.objects.filter(medico=m, fecha=manana, hora=h, estado='CANCELADA').delete()
    try:
        cita = Cita.objects.create(
            paciente=paciente,
            especialidad=m.especialidad,
            medico=m,
            fecha=manana,
            hora=h,
            codigo=codigo,
            estado='PROGRAMADA',
            tipo_cita='CONSULTA'
        )
    except IntegrityError:
        return JsonResponse({'ok': False, 'error': 'Slot ocupado'}, status=409)
    return JsonResponse({'ok': True, 'cita_id': cita.id, 'codigo': cita.codigo})

def orden_html(request, cita_id):
    c = get_object_or_404(Cita, id=cita_id)
    return render(request, 'citas/orden.html', {'cita': c})

def mis_citas(request):
    pid = request.session.get('paciente_id')
    if not pid:
        return redirect('citas:agendar')
    qs = Cita.objects.filter(paciente_id=pid).order_by('-fecha', 'hora')
    return render(request, 'citas/mis.html', {'citas': qs})

@require_POST
def editar_cita(request, cita_id):
    c = get_object_or_404(Cita, id=cita_id)
    pid = request.session.get('paciente_id')
    if c.paciente_id != pid:
        return HttpResponseBadRequest('No autorizado')
    return HttpResponseBadRequest('Para cambiar de horario debes cancelar la cita y agendar un nuevo horario')

@require_POST
def cancelar_cita(request, cita_id):
    c = get_object_or_404(Cita, id=cita_id)
    pid = request.session.get('paciente_id')
    if c.paciente_id != pid:
        return HttpResponseBadRequest('No autorizado')
    c.estado = 'CANCELADA'
    c.save(update_fields=['estado'])
    return JsonResponse({'ok': True})

def logout_paciente(request):
    request.session.pop('paciente_id', None)
    messages.info(request, 'Sesión de paciente cerrada')
    return redirect('home')

def home(request):
    ctx = {}
    pid = request.session.get('paciente_id')
    if pid:
        try:
            ctx['paciente'] = Paciente.objects.get(id=pid)
        except Paciente.DoesNotExist:
            request.session.pop('paciente_id', None)
    return render(request, 'home/home.html', ctx)


# =============================================
# VISTAS PARA MÉDICOS
# =============================================

@login_required
def citas_medico_hoy(request):
    """Vista para que el médico vea sus citas del día"""
    try:
        medico = request.user.medico
    except Medico.DoesNotExist:
        messages.error(request, 'No tienes perfil de médico')
        return redirect('home')
    
    hoy = datetime.now().date()
    citas = Cita.objects.filter(
        medico=medico,
        fecha=hoy,
        estado='PROGRAMADA'
    ).exclude(
        estado_atencion='ATENDIDO'
    ).order_by('hora').select_related('paciente', 'especialidad')
    
    ctx = {
        'medico': medico,
        'citas': citas,
        'fecha': hoy,
    }
    return render(request, 'citas/citas_medico.html', ctx)


@login_required
@require_POST
def iniciar_atencion(request, cita_id):
    """Endpoint para que el médico inicie la atención de un paciente"""
    try:
        medico = request.user.medico
    except Medico.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'No tienes perfil de médico'}, status=403)
    
    cita = get_object_or_404(Cita, id=cita_id, medico=medico)
    
    if cita.estado_atencion != 'EN_ESPERA':
        return JsonResponse({'ok': False, 'error': 'Esta cita no está en espera'}, status=400)
    
    cita.estado_atencion = 'EN_ATENCION'
    cita.tiempo_inicio_atencion = timezone.now()
    cita.save(update_fields=['estado_atencion', 'tiempo_inicio_atencion'])
    
    return JsonResponse({'ok': True, 'mensaje': 'Atención iniciada'})


@login_required
@require_POST
def finalizar_atencion(request, cita_id):
    """Endpoint para que el médico finalice la atención de un paciente"""
    try:
        medico = request.user.medico
    except Medico.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'No tienes perfil de médico'}, status=403)
    
    cita = get_object_or_404(Cita, id=cita_id, medico=medico)
    
    if cita.estado_atencion != 'EN_ATENCION':
        return JsonResponse({'ok': False, 'error': 'Esta cita no está en atención'}, status=400)
    
    cita.estado_atencion = 'ATENDIDO'
    cita.tiempo_fin_atencion = timezone.now()
    cita.duracion_atencion_minutos = cita.calcular_duracion()
    cita.save(update_fields=['estado_atencion', 'tiempo_fin_atencion', 'duracion_atencion_minutos'])
    
    return JsonResponse({
        'ok': True,
        'mensaje': 'Atención finalizada',
        'duracion': cita.duracion_atencion_minutos
    })


@login_required
@require_POST
def generar_codigo_ecografia(request, cita_id):
    """Endpoint para que el médico genere un código de ecografía para un paciente"""
    try:
        medico = request.user.medico
    except Medico.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'No tienes perfil de médico'}, status=403)
    
    cita = get_object_or_404(Cita, id=cita_id, medico=medico)
    
    # Generar código único para ecografía
    codigo = f"ECO{uuid.uuid4().hex[:6].upper()}"
    while Cita.objects.filter(codigo=codigo).exists():
        codigo = f"ECO{uuid.uuid4().hex[:6].upper()}"
    
    # Crear nueva cita de tipo ecografía con el código generado
    cita_ecografia = Cita.objects.create(
        paciente=cita.paciente,
        especialidad=cita.especialidad,
        medico=medico,
        fecha=cita.fecha,
        hora=cita.hora,
        codigo=codigo,
        estado='PROGRAMADA',
        tipo_cita='ECOGRAFIA'
    )
    
    return JsonResponse({
        'ok': True,
        'codigo': codigo,
        'mensaje': f'Código de ecografía generado: {codigo}'
    })


@login_required
@require_POST
def procesar_ecografia(request, cita_id):
    """Endpoint para habilitar o deshabilitar ecografía"""
    try:
        medico = request.user.medico
    except Medico.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'No tienes perfil de médico'}, status=403)
    
    try:
        cita = Cita.objects.get(id=cita_id, medico=medico)
    except Cita.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Cita no encontrada'}, status=404)
    
    habilitar = request.POST.get('habilitar') == 'si'
    
    # Validar que la cita fue procesada
    if cita.estado_atencion not in ['EN_ATENCION', 'ATENDIDO']:
        return JsonResponse({'ok': False, 'error': 'Esta cita no ha sido atendida'}, status=400)
    
    try:
        # Si aún no está finalizada, finalizar ahora
        if cita.estado_atencion == 'EN_ATENCION':
            cita.estado_atencion = 'ATENDIDO'
            cita.tiempo_fin_atencion = timezone.now()
            cita.duracion_atencion_minutos = cita.calcular_duracion()
        
        # Actualizar el campo de ecografía
        cita.requiere_ecografia = habilitar
        cita.save(update_fields=['estado_atencion', 'tiempo_fin_atencion', 'duracion_atencion_minutos', 'requiere_ecografia'])
        
        if habilitar:
            return JsonResponse({
                'ok': True,
                'mensaje': 'Ecografía habilitada para este paciente'
            })
        else:
            return JsonResponse({
                'ok': True,
                'mensaje': 'Ecografía no habilitada'
            })
    
    except Exception as e:
        return JsonResponse({'ok': False, 'error': f'Error al procesar: {str(e)}'}, status=500)


@login_required
def pacientes_atendidos(request):
    """Vista que muestra los pacientes atendidos por el médico"""
    try:
        medico = request.user.medico
    except Medico.DoesNotExist:
        messages.error(request, 'No tienes perfil de médico')
        return redirect('home')
    
    hoy = datetime.now().date()
    citas_atendidas = Cita.objects.filter(
        medico=medico,
        fecha=hoy,
        estado_atencion='ATENDIDO',
        estado='PROGRAMADA'
    ).order_by('-tiempo_fin_atencion').select_related('paciente', 'especialidad')
    
    ctx = {
        'medico': medico,
        'citas_atendidas': citas_atendidas,
        'fecha': hoy,
    }
    return render(request, 'citas/pacientes_atendidos.html', ctx)

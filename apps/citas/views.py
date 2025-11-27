from datetime import datetime, timedelta, time
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from apps.pacientes.models import Paciente
from apps.accounts.models import Medico
from apps.citas.models import Cita
from django.db import IntegrityError

def _manana():
    hoy = datetime.now().date()
    return hoy + timedelta(days=1)

def _slots_turno(turno):
    slots = []
    if turno == 'mannana':
        inicio, fin = time(8,0), time(12,0)
    elif turno == 'tarde':
        inicio, fin = time(14,0), time(18,0)
    else:
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
        return JsonResponse({'ok': False, 'error': 'Paciente no encontrado'}, status=404)
    request.session['paciente_id'] = p.id
    return JsonResponse({'ok': True, 'redirect': reverse('citas:agendar')})

@ensure_csrf_cookie
def agendar_inicio(request):
    pid = request.session.get('paciente_id')
    manana = _manana()
    medicos_manana = Medico.objects.filter(turnos__mannana=True)
    medicos_tarde = Medico.objects.filter(turnos__tarde=True)
    ctx = {
        'paciente_validado': bool(pid),
        'fecha_objetivo': manana,
        'medicos_manana': medicos_manana,
        'medicos_tarde': medicos_tarde,
    }
    return render(request, 'citas/agendar.html', ctx)

def agenda_medico(request, medico_id):
    m = get_object_or_404(Medico, id=medico_id)
    manana = _manana()
    turnos = []
    if m.turnos and m.turnos.mannana:
        turnos.append('mannana')
    if m.turnos and m.turnos.tarde:
        turnos.append('tarde')
    resultado = {}
    ocupados = set(Cita.objects.filter(medico=m, fecha=manana).exclude(estado='CANCELADA').values_list('hora', flat=True))
    for t in turnos:
        lista = []
        for h in _slots_turno(t):
            lista.append({
                'hora': h.strftime('%H:%M'),
                'ocupado': h in ocupados
            })
        resultado[t] = lista
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
    turno_ok = (m.turnos and ((m.turnos.mannana and time(8,0) <= h < time(12,0)) or (m.turnos.tarde and time(14,0) <= h < time(18,0))))
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
            estado='PROGRAMADA'
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

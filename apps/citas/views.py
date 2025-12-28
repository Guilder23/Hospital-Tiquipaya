from datetime import datetime, timedelta, time, date
import uuid
from io import BytesIO
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
from apps.especialidades.models import Especialidad
from django.db import IntegrityError
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

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


@login_required
def citas_index(request):
    """Vista principal del módulo de citas - muestra lista de citas según permisos"""
    user = request.user
    
    # Get citas based on user role
    if user.is_superuser or user.is_staff:
        # Admin sees all citas
        citas = Cita.objects.all().order_by('-fecha', '-hora')[:50]
    else:
        # Regular users see citas they created or are assigned to
        citas = Cita.objects.filter(
            fecha__gte=date.today()
        ).order_by('fecha', 'hora')[:50]
    
    context = {
        'citas': citas,
        'titulo': 'Gestión de Citas Médicas'
    }
    return render(request, 'citas/citas_index.html', context)


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

def _obtener_nombre_dia(fecha):
    """Obtiene el nombre del día de la semana (0=lunes, 6=domingo)"""
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    return dias[fecha.weekday()]

def _medico_trabaja_en_dia(medico, fecha):
    """Verifica si un médico trabaja en un día específico"""
    if not medico.dias_atencion:
        # Si no tiene días de atención configurados, asumimos que trabaja todos los días
        return True
    
    nombre_dia = _obtener_nombre_dia(fecha)
    dias_atencion = medico.dias_atencion
    
    # Mapear nombre del día al atributo correspondiente
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

@ensure_csrf_cookie
def agendar_inicio(request):
    pid = request.session.get('paciente_id')
    manana = _manana()
    
    # Obtener todos los turnos activos
    turnos_activos = Turnos.objects.filter(estado=True).order_by('hora_ini')
    
    # Para cada turno, obtener los médicos que trabajan en ese turno Y en el día siguiente
    turnos_data = []
    for turno in turnos_activos:
        # Filtrar médicos que trabajan en este turno
        medicos_turno = Medico.objects.filter(turnos=turno)
        
        # Filtrar médicos que trabajan en el día siguiente
        medicos_disponibles = [m for m in medicos_turno if _medico_trabaja_en_dia(m, manana)]
        
        turnos_data.append({
            'turno': turno,
            'medicos': medicos_disponibles
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
    qs = Cita.objects.filter(paciente_id=pid).select_related('medico__user__perfil', 'especialidad').order_by('-fecha', 'hora')
    especialidades = Especialidad.objects.all().order_by('nombre')
    return render(request, 'citas/mis.html', {'citas': qs, 'especialidades': especialidades})

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
    import sys
    # Limpiar completamente la sesión del paciente
    print(f"[LOGOUT] Antes - Session keys: {list(request.session.keys())}", flush=True)
    sys.stdout.flush()
    
    if 'paciente_id' in request.session:
        print(f"[LOGOUT] Eliminando paciente_id: {request.session['paciente_id']}", flush=True)
        del request.session['paciente_id']
    
    # Forzar guardado y flush de sesión
    request.session.modified = True
    request.session.save()
    
    print(f"[LOGOUT] Después - Session keys: {list(request.session.keys())}", flush=True)
    sys.stdout.flush()
    
    if request.method == 'POST':
        messages.info(request, 'Sesión de paciente cerrada')
    
    response = redirect('home')
    # Prevenir caché del navegador
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['Clear-Site-Data'] = '"cache"'
    print("[LOGOUT] Redirect response creado", flush=True)
    sys.stdout.flush()
    return response

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
    
    # Obtener todas las ecografías activas del sistema
    ecografias = Ecografia.objects.filter(estado='ACTIVA')
    
    ctx = {
        'medico': medico,
        'citas': citas,
        'fecha': hoy,
        'ecografias': ecografias,
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
            
            # Debug: verificar tiempos
            print(f"DEBUG procesar_ecografia: tiempo_inicio={cita.tiempo_inicio_atencion}, tiempo_fin={cita.tiempo_fin_atencion}")
            
            cita.duracion_atencion_minutos = cita.calcular_duracion()
            print(f"DEBUG procesar_ecografia: duracion_calculada={cita.duracion_atencion_minutos}")
        
        # Actualizar el campo de ecografía y datos relacionados
        cita.requiere_ecografia = habilitar
        
        if habilitar:
            # Obtener ecografía y comentario si se habilita ecografía
            ecografia_id = request.POST.get('ecografia')
            comentario = request.POST.get('comentario')
            
            print(f"DEBUG: ecografia_id={ecografia_id}, comentario={comentario}")
            
            if not ecografia_id:
                return JsonResponse({'ok': False, 'error': 'La ecografía es requerida'}, status=400)
            
            if not comentario or not comentario.strip():
                return JsonResponse({'ok': False, 'error': 'El comentario es requerido'}, status=400)
            
            try:
                ecografia = Ecografia.objects.get(id=ecografia_id)
                # Guardar referencia a la ecografía
                cita.ecografia = ecografia
                cita.comentario_ecografia = comentario
                print(f"DEBUG: Ecografía guardada: {ecografia.nombre}, Comentario: {comentario}")
            except Ecografia.DoesNotExist:
                return JsonResponse({'ok': False, 'error': 'Ecografía no válida'}, status=400)
        
        cita.save(update_fields=['estado_atencion', 'tiempo_fin_atencion', 'duracion_atencion_minutos', 'requiere_ecografia', 'ecografia', 'comentario_ecografia'])
        
        print(f"DEBUG: Cita guardada. requiere_ecografia={cita.requiere_ecografia}, comentario_ecografia={cita.comentario_ecografia}")
        
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
        print(f"ERROR: {str(e)}")
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


# =============================================
# VISTAS PARA AGENDAMIENTO POR USUARIOS DEL SISTEMA
# (Admin, Recepción, Encargado de Admisión, etc.)
# =============================================

@login_required
@login_required
def agendar_cita_usuario(request):
    """Vista para que usuarios autenticados (admin, recepción, etc.) agenden citas"""
    manana = _manana()
    
    # Obtener todos los turnos activos
    turnos_activos = Turnos.objects.filter(estado=True).order_by('hora_ini')
    
    # Para cada turno, obtener los médicos que trabajan en ese turno Y en el día siguiente
    turnos_data = []
    for turno in turnos_activos:
        # Filtrar médicos que trabajan en este turno
        medicos_turno = Medico.objects.filter(turnos=turno)
        
        # Filtrar médicos que trabajan en el día siguiente
        medicos_disponibles = [m for m in medicos_turno if _medico_trabaja_en_dia(m, manana)]
        
        turnos_data.append({
            'turno': turno,
            'medicos': medicos_disponibles
        })
    
    ctx = {
        'fecha_objetivo': manana,
        'turnos_data': turnos_data,
        'usuario_creador': request.user,
    }
    return render(request, 'citas/agendar_usuario.html', ctx)


@login_required
def buscar_paciente_usuario(request):
    """API endpoint para buscar pacientes por CI o nombre"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'pacientes': []})
    
    from django.db.models import Q
    pacientes = Paciente.objects.filter(
        Q(ci__icontains=query) | 
        Q(nombres__icontains=query) | 
        Q(apellido_paterno__icontains=query),
        activo=True
    ).values('id', 'ci', 'nombres', 'apellido_paterno', 'fecha_nacimiento')[:20]
    
    return JsonResponse({
        'pacientes': list(pacientes)
    })


@login_required
@require_POST
def confirmar_cita_usuario(request):
    """Confirmar cita agendada por usuario autenticado"""
    paciente_id = request.POST.get('paciente_id')
    medico_id = request.POST.get('medico_id')
    hora_str = request.POST.get('hora')
    
    if not all([paciente_id, medico_id, hora_str]):
        return JsonResponse({'ok': False, 'error': 'Datos incompletos'}, status=400)
    
    try:
        paciente = Paciente.objects.get(id=paciente_id, activo=True)
        medico = Medico.objects.get(id=medico_id)
    except (Paciente.DoesNotExist, Medico.DoesNotExist):
        return JsonResponse({'ok': False, 'error': 'Paciente o médico no encontrado'}, status=404)
    
    manana = _manana()
    
    try:
        h = datetime.strptime(hora_str, '%H:%M').time()
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Hora inválida'}, status=400)
    
    # Validar que el paciente no tenga otra cita el mismo día
    if Cita.objects.filter(paciente=paciente, fecha=manana).exclude(estado='CANCELADA').exists():
        return JsonResponse({'ok': False, 'error': 'Este paciente ya tiene una cita agendada para mañana'}, status=409)
    
    # Validar que la hora está dentro de los turnos del médico
    turno_ok = False
    for turno in medico.turnos.filter(estado=True):
        if turno.hora_ini <= h < turno.hora_fin:
            turno_ok = True
            break
    
    if not turno_ok:
        return JsonResponse({'ok': False, 'error': 'Hora fuera de turno'}, status=400)
    
    # Validar que la hora no esté ocupada
    if Cita.objects.filter(medico=medico, fecha=manana, hora=h).exclude(estado='CANCELADA').exists():
        return JsonResponse({'ok': False, 'error': 'El slot ya está ocupado'}, status=409)
    
    # Generar código
    codigo = _generar_codigo_unico('CITA')
    
    # Eliminar registros cancelados del mismo slot
    Cita.objects.filter(medico=medico, fecha=manana, hora=h, estado='CANCELADA').delete()
    
    try:
        cita = Cita.objects.create(
            paciente=paciente,
            especialidad=medico.especialidad,
            medico=medico,
            fecha=manana,
            hora=h,
            codigo=codigo,
            estado='PROGRAMADA',
            tipo_cita='CONSULTA',
            usuario_creador=request.user  # Registrar quién creó la cita
        )
        
        return JsonResponse({
            'ok': True,
            'cita_id': cita.id,
            'codigo': cita.codigo,
            'mensaje': f'Cita agendada exitosamente para {paciente.nombres}'
        })
    except IntegrityError:
        return JsonResponse({'ok': False, 'error': 'Error al agendar la cita (slot ocupado)'}, status=409)

def generar_pdf_cita(request, cita_id):
    """Genera una orden de cita médica en PDF para el paciente"""
    cita = get_object_or_404(Cita, id=cita_id)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.4 * inch,
        bottomMargin=0.4 * inch,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch
    )

    elementos = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados (reducidos)
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
    
    # Encabezado
    elementos.append(Paragraph('<b>HOSPITAL TIQUIPAYA</b>', titulo_style))
    elementos.append(Paragraph('Orden de Cita Médica', subtitulo_style))
    
    # Línea separadora
    line_table = Table([['']], colWidths=[7 * inch])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#1e5a7d')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(line_table)
    
    # Información de la cita
    elementos.append(Paragraph('<b>INFORMACIÓN DE LA CITA</b>', seccion_style))
    
    datos_cita = [
        ['Número de Orden:', f'CM-{cita.id:06d}'],
        ['Fecha de Emisión:', date.today().strftime('%d/%m/%Y')],
        ['Código de Cita:', cita.codigo or 'No asignado'],
        ['Estado:', cita.estado],
    ]
    
    tabla_cita = Table(datos_cita, colWidths=[2.3 * inch, 4.2 * inch])
    tabla_cita.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#bdc3c7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elementos.append(tabla_cita)
    
    # Datos del paciente
    elementos.append(Paragraph('<b>DATOS DEL PACIENTE</b>', seccion_style))
    
    datos_paciente = [
        ['Nombre Completo:', f'{cita.paciente.nombres} {cita.paciente.apellido_paterno} {cita.paciente.apellido_materno}'],
        ['CI:', cita.paciente.ci or 'No registrado'],
        ['Fecha de Nacimiento:', cita.paciente.fecha_nacimiento.strftime('%d/%m/%Y') if cita.paciente.fecha_nacimiento else 'No registrada'],
        ['Teléfono:', cita.paciente.celular or 'No registrado'],
    ]
    
    tabla_paciente = Table(datos_paciente, colWidths=[2.3 * inch, 4.2 * inch])
    tabla_paciente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#a5d6a7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elementos.append(tabla_paciente)
    
    # Detalles médicos
    elementos.append(Paragraph('<b>DETALLES DE LA ATENCIÓN MÉDICA</b>', seccion_style))
    
    datos_medicos = [
        ['Especialidad:', cita.especialidad.nombre],
        ['Médico:', f'Dr(a). {cita.medico.user.perfil.nombres} {cita.medico.user.perfil.apellido_paterno}'],
        ['Consultorio:', cita.medico.consultorio or 'No asignado'],
        ['Fecha de Cita:', cita.fecha.strftime('%d/%m/%Y')],
        ['Hora de Cita:', cita.hora.strftime('%H:%M')],
    ]
    
    tabla_medica = Table(datos_medicos, colWidths=[2.3 * inch, 4.2 * inch])
    tabla_medica.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#90caf9')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elementos.append(tabla_medica)
    
    # Ecografía
    if cita.requiere_ecografia and cita.ecografia:
        elementos.append(Paragraph('<b>INDICACIÓN DE ECOGRAFÍA</b>', seccion_style))
        
        datos_eco = [['Tipo de Ecografía:', cita.ecografia.nombre]]
        if cita.comentario_ecografia:
            datos_eco.append(['Observaciones:', cita.comentario_ecografia])
        
        tabla_eco = Table(datos_eco, colWidths=[2.3 * inch, 4.2 * inch])
        tabla_eco.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff9c4')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#fff59d')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elementos.append(tabla_eco)
    
    # Instrucciones
    instrucciones_style = ParagraphStyle(
        'Instrucciones',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#e74c3c'),
        leading=11,
        leftIndent=15,
        rightIndent=15
    )
    
    elementos.append(Paragraph(
        '<b>INSTRUCCIONES IMPORTANTES:</b><br/>'
        '• Presentarse 15 minutos antes<br/>'
        '• Traer carnet de identidad<br/>'
        '• Traer esta orden impresa o digital<br/>'
        '• Cancelar si no puede asistir',
        instrucciones_style
    ))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER,
        spaceBefore=10
    )
    
    elementos.append(Paragraph(
        'Hospital Tiquipaya - Servicio de Atención Médica<br/>'
        f'Generado el {date.today().strftime("%d/%m/%Y")}',
        footer_style
    ))
    
    doc.build(elementos)
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orden_cita_{cita.id}_{cita.paciente.ci}.pdf"'
    response.write(pdf)
    
    return response


# horarios/views.py (Adaptado para roles)

from django.views.generic import ListView
from django.views import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin # Agregamos LoginRequiredMixin
from django.contrib import messages
import json
from django.shortcuts import render, redirect
from .models import HorarioSistema
from django import forms

# Asegúrate de que este import sea correcto
from apps.accounts.models import Perfil 
from apps.permisos.utils import es_admin_o_staff
from .models import Turnos
from apps.permisos.models import Modulo, Permiso
from apps.accounts.models import TipoUsuario

# --- FUNCIÓN DE PERMISOS ---
def _es_admin(user):
    return es_admin_o_staff(user)

# --- VISTA PARA LA PLANTILLA (Template View) ---
class TurnoListView(LoginRequiredMixin, ListView): # Hereda de LoginRequiredMixin
    """Muestra la tabla de turnos."""
    model = Turnos
    template_name = 'turnos/turnos.html' # Asegúrate que este es el nombre de tu template
    context_object_name = 'lista_turnos'

    def get_context_data(self, **kwargs):
        """Añade la variable permiso_actual al contexto para el template."""
        ctx = super().get_context_data(**kwargs)
        # Inyectamos la variable que usaste en tu template
        ctx['permiso_actual'] = getattr(self.request, 'permiso_actual', None)
        return ctx

# --- VISTA PARA LA API (AJAX CRUD) ---
@method_decorator(csrf_exempt, name='dispatch')
class TurnoAPIView(View):
    """
    Vista que maneja las peticiones AJAX/JSON para Crear, Editar y Eliminar (POST, PATCH, DELETE).
    (Nota: Se debería agregar aquí una verificación de permisos en entornos de producción.)
    """

    # Obtener un turno específico (no estrictamente necesario si usamos data-*)
    def get(self, request, pk=None):
        if pk:
            try:
                turno = Turnos.objects.get(pk=pk)
                data = model_to_dict(turno)
                data['hora_ini'] = turno.hora_ini.strftime('%H:%M')
                data['hora_fin'] = turno.hora_fin.strftime('%H:%M')
                return JsonResponse(data)
            except Turnos.DoesNotExist:
                return JsonResponse({'error': 'Turno no encontrado'}, status=404)
        return JsonResponse({'error': 'ID requerido'}, status=400)

    # Crear un nuevo turno (C)
    def post(self, request):
        permiso = getattr(request, 'permiso_actual', None)
        if not (permiso and permiso.puede_editar()):
            return JsonResponse({'error': 'No tienes permiso para crear'}, status=403)
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ('nombre', 'hora_ini', 'hora_fin')):
                return JsonResponse({'error': 'Datos incompletos'}, status=400)
            
            turno = Turnos.objects.create(
                nombre=data['nombre'],
                hora_ini=data['hora_ini'],
                hora_fin=data['hora_fin']
            )
            msg = f'Turno "{turno.nombre}" creado correctamente.'
            messages.success(request, msg)
            return JsonResponse({**model_to_dict(turno), 'message': msg}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # Editar un turno (U) - Usaremos PATCH para actualizar campos específicos
    def patch(self, request, pk):
        permiso = getattr(request, 'permiso_actual', None)
        if not (permiso and permiso.puede_editar()):
            return JsonResponse({'error': 'No tienes permiso para editar'}, status=403)
        try:
            turno = Turnos.objects.get(pk=pk)
        except Turnos.DoesNotExist:
            return JsonResponse({'error': 'Turno no encontrado'}, status=404)
        
        try:
            data = json.loads(request.body)

            if 'estado' in data:
                turno.estado = data['estado']
            
            if 'nombre' in data:
                turno.nombre = data['nombre']
            if 'hora_ini' in data:
                turno.hora_ini = data['hora_ini']
            if 'hora_fin' in data:
                turno.hora_fin = data['hora_fin']
                
            turno.save()
            msg = f'Turno "{turno.nombre}" editado correctamente.'
            messages.success(request, msg)
            return JsonResponse({**model_to_dict(turno), 'message': msg})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # Eliminar un turno (D)
    def delete(self, request, pk):
        permiso = getattr(request, 'permiso_actual', None)
        if not (permiso and permiso.puede_editar()):
            return JsonResponse({'error': 'No tienes permiso para eliminar'}, status=403)
        try:
            turno = Turnos.objects.get(pk=pk)
            turno.estado = False  # Lo deshabilita
            turno.save()
            msg = f'Turno "{turno.nombre}" deshabilitado con éxito'
            messages.success(request, msg)
            return JsonResponse({'message': msg})
        except Turnos.DoesNotExist:
            return JsonResponse({'error': 'Turno no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# --- FORMULARIO Y VISTA PARA GESTIONAR HORARIO GLOBAL ---
class HorarioSistemaForm(forms.ModelForm):
    class Meta:
        model = HorarioSistema
        fields = ['hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class HorarioSistemaView(LoginRequiredMixin, View):
    template_name = 'horarios/gestionar_horario.html'

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario es admin o staff
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        
        # Verificar permiso de edición para el módulo de horarios
        tipo_usuario = None
        if hasattr(request.user, 'perfil') and request.user.perfil:
            tipo_usuario = request.user.perfil.tipo
        
        if tipo_usuario:
            try:
                modulo = Modulo.objects.get(nombre__icontains='Gestionar horarios para citas')
                permiso = Permiso.objects.filter(tipo_usuario=tipo_usuario, modulo=modulo).first()
                if permiso and permiso.tipo_permiso == 'editor':
                    return super().dispatch(request, *args, **kwargs)
            except Modulo.DoesNotExist:
                pass
        
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('dashboard:dashboard')

    def get(self, request):
        horario = HorarioSistema.objects.first()
        form = HorarioSistemaForm(instance=horario)
        return render(request, self.template_name, {'form': form, 'horario': horario})

    def post(self, request):
        horario = HorarioSistema.objects.first()
        form = HorarioSistemaForm(request.POST, instance=horario)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.actualizado_por = request.user
            horario.save()
            messages.success(request, 'Horario actualizado correctamente.')
            return redirect('turnos:gestionar')
        return render(request, self.template_name, {'form': form, 'horario': horario})
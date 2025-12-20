from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Especialidad
from django.contrib import messages

@login_required
def lista_especialidades(request):
    especialidades = Especialidad.objects.all()
    permiso = getattr(request, 'permiso_actual', None)
    return render(request, 'specialties/specialties.html', {
        'especialidades': especialidades,
        'permiso_actual': permiso
    })

@login_required
def crear_especialidad(request):
    permiso = getattr(request, 'permiso_actual', None)
    if not (permiso and permiso.puede_editar()):
        messages.error(request, "No tienes permiso para crear especialidades")
        return redirect('lista_especialidades')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        try:
            Especialidad.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, "Especialidad creada correctamente.")
            return redirect('lista_especialidades')
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, 'specialties/create.html')

@login_required
def editar_especialidad(request, id):
    permiso = getattr(request, 'permiso_actual', None)
    if not (permiso and permiso.puede_editar()):
        messages.error(request, "No tienes permiso para editar especialidades")
        return redirect('lista_especialidades')
    
    especialidad = get_object_or_404(Especialidad, id=id)

    if request.method == 'POST':
        especialidad.nombre = request.POST.get('nombre')
        especialidad.descripcion = request.POST.get('descripcion')
        especialidad.save()
        messages.success(request, "Especialidad actualizada.")
        return redirect('lista_especialidades')

    return render(request, 'specialties/edit.html', {'especialidad': especialidad})

@login_required
def activar_especialidad(request, id):
    permiso = getattr(request, 'permiso_actual', None)
    if not (permiso and permiso.puede_editar()):
        messages.error(request, "No tienes permiso para activar especialidades")
        return redirect('lista_especialidades')
    
    especialidad = get_object_or_404(Especialidad, id=id)
    especialidad.estado = True
    especialidad.save()
    return redirect('lista_especialidades')

@login_required
def desactivar_especialidad(request, id):
    permiso = getattr(request, 'permiso_actual', None)
    if not (permiso and permiso.puede_editar()):
        messages.error(request, "No tienes permiso para desactivar especialidades")
        return redirect('lista_especialidades')

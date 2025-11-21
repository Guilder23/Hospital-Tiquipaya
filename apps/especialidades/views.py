from django.shortcuts import render, redirect, get_object_or_404
from .models import Especialidad
from django.contrib import messages

def lista_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'specialties/specialties.html', {'especialidades': especialidades})

def crear_especialidad(request):
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

def editar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)

    if request.method == 'POST':
        especialidad.nombre = request.POST.get('nombre')
        especialidad.descripcion = request.POST.get('descripcion')
        especialidad.save()
        messages.success(request, "Especialidad actualizada.")
        return redirect('lista_especialidades')

    return render(request, 'specialties/edit.html', {'especialidad': especialidad})

def activar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    especialidad.estado = True
    especialidad.save()
    return redirect('lista_especialidades')

def desactivar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    especialidad.estado = False
    especialidad.save()
    return redirect('lista_especialidades')

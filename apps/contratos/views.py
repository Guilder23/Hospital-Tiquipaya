from django.views.generic import ListView
from django.views import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from apps.accounts.models import Perfil
from .models import Contrato

def _es_admin(user):
    if user.is_superuser or user.is_staff:
        return True
    try:
        perfil = user.perfil
    except Perfil.DoesNotExist:
        return False
    if perfil.tipo is None:
        return False
    return perfil.tipo.nombre.lower() == 'administrador'

class ContratoListView(ListView):
    model = Contrato
    template_name = 'contratos/contratos.html'
    context_object_name = 'lista_contratos'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['puede_admin'] = _es_admin(self.request.user)
        return ctx

@method_decorator(csrf_exempt, name='dispatch')
class ContratoAPIView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                contrato = Contrato.objects.get(pk=pk)
                data = model_to_dict(contrato)
                return JsonResponse(data)
            except Contrato.DoesNotExist:
                return JsonResponse({'error': 'Contrato no encontrado'}, status=404)
        return JsonResponse({'error': 'ID requerido'}, status=400)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ('nombre','fecha_inicio','fecha_fin')):
                return JsonResponse({'error': 'Datos incompletos'}, status=400)
            contrato = Contrato.objects.create(
                nombre=data['nombre'],
                fecha_inicio=data['fecha_inicio'],
                fecha_fin=data['fecha_fin']
            )
            return JsonResponse(model_to_dict(contrato), status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def patch(self, request, pk):
        try:
            contrato = Contrato.objects.get(pk=pk)
        except Contrato.DoesNotExist:
            return JsonResponse({'error': 'Contrato no encontrado'}, status=404)

        try:
            data = json.loads(request.body)
            if 'estado' in data:
                contrato.estado = data['estado']
            if 'nombre' in data:
                contrato.nombre = data['nombre']
            if 'fecha_inicio' in data:
                contrato.fecha_inicio = data['fecha_inicio']
            if 'fecha_fin' in data:
                contrato.fecha_fin = data['fecha_fin']
            contrato.save()
            return JsonResponse(model_to_dict(contrato))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, pk):
        try:
            contrato = Contrato.objects.get(pk=pk)
            contrato.estado = False
            contrato.save()
            return JsonResponse({'message': 'Contrato deshabilitado con éxito'})
        except Contrato.DoesNotExist:
            return JsonResponse({'error': 'Contrato no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


from django.core.management.base import BaseCommand
from apps.permisos.models import Modulo


class Command(BaseCommand):
    help = 'Inicializa el módulo de gestión de horarios para citas'

    def handle(self, *args, **options):
        modulo, created = Modulo.objects.get_or_create(
            nombre='Gestionar horarios para citas',
            defaults={
                'descripcion': 'Permite configurar el horario global del sistema de citas',
                'icono': 'fas fa-clock',
                'url': '/horarios/gestionar-horario/',
                'orden': 50,
                'activo': True,
                'asignable': True,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Módulo "{modulo.nombre}" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠ El módulo "{modulo.nombre}" ya existe')
            )

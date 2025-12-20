from django.core.management.base import BaseCommand
from apps.permisos.models import Modulo

class Command(BaseCommand):
    help = "Lista los nombres de Modulo existentes"

    def handle(self, *args, **options):
        self.stdout.write('MÓDULOS EXISTENTES:')
        for m in Modulo.objects.all().order_by('orden'):
            self.stdout.write(f"- {m.nombre} → {m.url}")

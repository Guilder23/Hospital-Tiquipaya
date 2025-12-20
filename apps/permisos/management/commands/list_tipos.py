from django.core.management.base import BaseCommand
from apps.accounts.models import TipoUsuario

class Command(BaseCommand):
    help = "Lista los tipos de usuario existentes"

    def handle(self, *args, **options):
        self.stdout.write('TIPOS DE USUARIO EXISTENTES:')
        for tipo in TipoUsuario.objects.all():
            self.stdout.write(f"- {tipo.nombre}")

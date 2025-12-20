from django.core.management.base import BaseCommand
from apps.permisos.models import Modulo, Permiso
from apps.accounts.models import TipoUsuario

class Command(BaseCommand):
    help = "Resetea módulos por defecto y permisos para Medico y Ecografo (deja exactamente 3 opciones visibles)"

    def handle(self, *args, **options):
        # Definición por URL para evitar problemas de acentos/encoding
        roles_urls = {
            'Medico': ['/home/', '/citas/medico/hoy/', '/citas/medico/atendidos/'],
            'Ecografo': ['/home/', '/citas-ecografia/mis-citas/', '/citas-ecografia/pacientes-atendidos/'],
            'Encargado de Admision': ['/home/', '/pacientes/'],
            'Recepcion de Admision': ['/home/', '/pacientes/'],
        }

        self.stdout.write('='*60)
        self.stdout.write('RESETEANDO MÓDULOS POR DEFECTO Y PERMISOS')
        self.stdout.write('='*60)

        mods_by_url = {m.url: m for m in Modulo.objects.all()}

        for role_name, default_urls in roles_urls.items():
            try:
                tipo = TipoUsuario.objects.get(nombre=role_name)
            except TipoUsuario.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"TipoUsuario no encontrado: {role_name}"))
                continue

            # Reset defaults
            tipo.modulos_por_defecto.clear()
            for url in default_urls:
                mod = mods_by_url.get(url)
                if mod:
                    tipo.modulos_por_defecto.add(mod)
                    self.stdout.write(self.style.SUCCESS(f"{role_name}: por defecto → {mod.nombre} ({url})"))
                else:
                    self.stdout.write(self.style.WARNING(f"Módulo no existe con URL: {url}"))

            allowed_urls = set(default_urls)

            # Reset permisos: todo lo no permitido → sin acceso e invisible
            for m in Modulo.objects.all():
                if m.url not in allowed_urls:
                    Permiso.objects.update_or_create(
                        tipo_usuario=tipo,
                        modulo=m,
                        defaults={'visible': False, 'tipo_permiso': 'sin_acceso'}
                    )
            self.stdout.write(self.style.SUCCESS(f"{role_name}: permisos restantes en sin acceso"))

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('PROCESO COMPLETADO'))
        self.stdout.write('='*60)

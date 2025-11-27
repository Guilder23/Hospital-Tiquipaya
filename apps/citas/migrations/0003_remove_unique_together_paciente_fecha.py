from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0002_add_medico_codigo_constraints'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cita',
            unique_together=set(),
        ),
    ]


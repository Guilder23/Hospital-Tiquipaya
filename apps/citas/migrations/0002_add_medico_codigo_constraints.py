from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0001_initial'),
        ('accounts', '0005_especialidad_admision_encargadoadmision_medico_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='medico',
            field=models.ForeignKey(default=None, on_delete=models.deletion.CASCADE, to='accounts.medico'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cita',
            name='codigo',
            field=models.CharField(default='TEMP', max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='cita',
            constraint=models.UniqueConstraint(fields=('medico','fecha','hora'), name='cita_unica_por_medico_slot'),
        ),
    ]


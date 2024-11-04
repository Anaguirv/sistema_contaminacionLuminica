# Generated by Django 5.0.7 on 2024-11-04 00:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inspectores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentoMedicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('0', 'Luxómetro'), ('1', 'Luminancímetro')], max_length=1, verbose_name='Iipo')),
                ('marca', models.CharField(max_length=50, verbose_name='Marca')),
                ('modelo', models.CharField(max_length=50, verbose_name='Modelo')),
                ('num_serie', models.CharField(max_length=50, verbose_name='N° de Serie')),
            ],
            options={
                'verbose_name': 'Instrumento de medición',
                'verbose_name_plural': 'Instrumentos de medición',
                'db_table': 'instrumento_medicion',
            },
        ),
        migrations.CreateModel(
            name='Medicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cumplimiento', models.CharField(blank=True, choices=[('0', 'No'), ('1', 'Si')], max_length=1, null=True, verbose_name='Cumplimiento')),
                ('latitud', models.FloatField(verbose_name='Latitud')),
                ('longitud', models.FloatField(verbose_name='Longitud')),
                ('temperatura', models.FloatField(verbose_name='Temperatura (°C)')),
                ('humedad', models.FloatField(verbose_name='Humedad (%)')),
                ('valor_medido', models.FloatField(verbose_name='Valor medido')),
                ('observacion', models.CharField(max_length=500, verbose_name='Observación')),
                ('creado', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('inspector', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='inspectores.inspector')),
                ('instrumento_medicion', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='catalogo_mediciones.instrumentomedicion')),
            ],
            options={
                'verbose_name': 'Medición',
                'verbose_name_plural': 'Mediciones',
                'db_table': 'medicion',
            },
        ),
    ]

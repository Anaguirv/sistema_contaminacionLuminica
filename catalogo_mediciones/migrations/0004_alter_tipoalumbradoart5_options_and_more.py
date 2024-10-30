# Generated by Django 5.0.7 on 2024-10-26 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo_mediciones', '0003_alter_tipoalumbradoart5_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipoalumbradoart5',
            options={'verbose_name': 'Medicion art5', 'verbose_name_plural': 'Mediciones art5'},
        ),
        migrations.AlterModelOptions(
            name='tipoalumbradoart6',
            options={'verbose_name': 'Medicion art6', 'verbose_name_plural': 'Mediciones art6'},
        ),
        migrations.RenameField(
            model_name='tipoalumbradoart6',
            old_name='hemisferio_superior',
            new_name='Hemisferio_superior',
        ),
        migrations.RemoveField(
            model_name='catalogomedicion',
            name='creado',
        ),
        migrations.AlterField(
            model_name='tipoalumbradoart6',
            name='horario_extendido',
            field=models.CharField(max_length=2, verbose_name='Permiso de extención horaria'),
        ),
        migrations.AlterField(
            model_name='tipoalumbradoart6',
            name='limite_horario',
            field=models.CharField(max_length=2, verbose_name='Limite horario'),
        ),
    ]
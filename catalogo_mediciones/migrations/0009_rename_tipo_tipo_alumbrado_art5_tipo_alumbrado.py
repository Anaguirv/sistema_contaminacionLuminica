# Generated by Django 5.0.7 on 2024-10-22 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo_mediciones', '0008_tipo_alumbrado_art6'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tipo_alumbrado_art5',
            old_name='tipo',
            new_name='tipo_alumbrado',
        ),
    ]
# Generated by Django 4.2 on 2025-03-24 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='producto',
        ),
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to='web.categoria'),
            preserve_default=False,
        ),
    ]

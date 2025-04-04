# Generated by Django 4.2 on 2025-03-28 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_cliente_profile'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='producto',
        ),
        migrations.AddField(
            model_name='cart',
            name='FEE',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.producto')),
            ],
        ),
    ]

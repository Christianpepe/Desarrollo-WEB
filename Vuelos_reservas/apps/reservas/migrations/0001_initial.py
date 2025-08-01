# Generated by Django 4.2.7 on 2025-06-30 00:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vuelos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_reserva', models.CharField(max_length=10, unique=True)),
                ('estado', models.CharField(default='pendiente', max_length=20)),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_reserva', models.DateTimeField(auto_now_add=True)),
                ('fecha_expiracion', models.DateTimeField(blank=True, null=True)),
                ('pasajeros_total', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vuelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vuelos.vuelo')),
            ],
        ),
        migrations.CreateModel(
            name='Pasajero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=100)),
                ('tipo_documento', models.CharField(max_length=30)),
                ('numero_documento', models.CharField(max_length=30)),
                ('fecha_nacimiento', models.DateField()),
                ('nacionalidad', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('equipaje_adicional', models.BooleanField(default=False)),
                ('comida_especial', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('asiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vuelos.asiento')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.reserva')),
            ],
        ),
    ]

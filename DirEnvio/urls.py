from django.urls import path
from . import views

app_name = 'Envio'

urlpatterns=[
    path('', views.EnvioDirecciones.as_view(), name='direccion_envio'),
    path('nueva', views.FormularioDir, name='nueva'),
]


from django.urls import path
from . import views

app_name = 'orden'

urlpatterns =[
    path('', views.orden, name='orden'),
    path('direccion', views.direccion, name='direccion'),
    path('seleccionar/direccion', views.seleccionar_direccion, name='seleccionar_envio'),
    path('cambio/direccion/<int:pk>', views.check_direccion, name='cambiar')
    
]
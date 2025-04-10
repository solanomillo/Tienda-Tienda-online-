from django.urls import path
from . import views

app_name = 'orden'

urlpatterns =[
    path('', views.orden, name='orden'),
    path('direccion', views.direccion, name='direccion'),
    path('seleccionar/direccion', views.seleccionar_direccion, name='seleccionar_envio'),
    path('cambio/direccion/<int:pk>', views.check_direccion, name='cambiar'),
    path('confirmacion', views.confirmacion, name='confirmacion'),
    path('cancelar', views.cancelar_orden, name='cancelar'),
    path('completado', views.completado, name='completado'),
    path('ordenes/completadas', views.OrdenView.as_view(), name='historial'), 
]
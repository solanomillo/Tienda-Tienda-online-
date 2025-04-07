from django.urls import path
from . import views

app_name = 'Envio'

urlpatterns=[
    path('', views.EnvioDirecciones.as_view(), name='direccion_envio'),
    path('nueva', views.FormularioDir, name='nueva'),
    path('actualizar/<int:pk>', views.UpdateDireccion.as_view(), name='actualizar'),
    path('Eliminar/<int:pk>', views.DeleteDireccion.as_view(), name='Eliminar'),
    path('principal/<int:pk>', views.funcDefault, name='principal')
]


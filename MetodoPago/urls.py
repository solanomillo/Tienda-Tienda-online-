from django.urls import path
from .  import views

app_name = 'MetodoPago'

urlpatterns = [
    path('', views.metodo_pago, name='metodo_pago'),
]
from django.urls import path
from . import views

app_name = 'promo_codigo'

urlpatterns = [
    path('', views.validar, name='validar'),
]
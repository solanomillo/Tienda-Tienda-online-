from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login/',views.login, name='login'),
    path('logout/', views.salir, name='logout'),
    path('registro', views.registro, name='registro'),    
]
from django.urls import path
from . import views


app_name= 'cart'

urlpatterns =[
    path('', views.cart, name='carrito'),
    path('agregarCarrito/<int:producto_id>/', views.agregarCarrito, name='agregarCarrito'),
    path('eliminar/<slug:slug>', views.eliminarProductoCarrito, name='eliminar'),
    path('vaciar', views.vaciarCarrito, name='vaciar'),    
]
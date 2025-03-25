from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [    
    path('buscar', views.BuscarProductoListView.as_view(), name='buscar'),
    path('productosPorCategoria/<slug:slug>/',views.ProductosPorCategoriaListView.as_view(), name='productosPorCategoria'),
    path('',views.ProductoListView.as_view(), name='index'),
    path('producto/<slug:slug>/', views.ProductoDetalleView.as_view(), name='productoDetalle'),
    path('login/',views.userLogin, name='login'),
    path('logout/', views.salir, name='logout'),
    path('registro/', views.registro, name='registro'),    
]
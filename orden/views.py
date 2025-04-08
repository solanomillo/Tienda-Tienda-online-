from django.shortcuts import get_object_or_404, redirect, render
from carts.funCart import funcionCarrito
from .utils import funcionOrden, breadcrumb
from django.contrib.auth.decorators import login_required
from DirEnvio.models import DireccionEnvio

@login_required(login_url='web:login')
def orden(request):
    cart = funcionCarrito(request)
    orden = funcionOrden(cart, request)
        
    return render(request, 'orden.html', {
        'orden':orden,
        'cart': cart,
        'breadcrumb': breadcrumb(products=True),
    })



@login_required(login_url='web:login')
def direccion(request):
    cart = funcionCarrito(request)
    orden = funcionOrden(cart, request)
    
    direccion_envio = orden.get_or_set_direccion_envio()
    
    countDireccion = request.user.direcciones.count() > 1
    
    return render(request, 'direccion.html', {
        'cart':cart,
        'orden':orden,
        'direccion_envio': direccion_envio,
        'countDireccion': countDireccion,
        'breadcrumb':breadcrumb(address=True)
    })
    
    
@login_required(login_url='web:login')
def seleccionar_direccion(request):
    
    direccion_envios = request.user.direcciones.all()
    
    return render(request, 'seleccionar.html',{
        'breadcrumb':breadcrumb(address=True),
        'direccion_envios':direccion_envios
    })
    

@login_required(login_url='web:login')
def check_direccion(request, pk):
    cart = funcionCarrito(request)
    orden = funcionOrden(cart, request)
    
    direccion_envio = get_object_or_404(DireccionEnvio, pk=pk)
    
    if request.user.id != direccion_envio.user_id:
        return redirect('web:index')
    
    orden.update_direccion_envio(direccion_envio)
    
    return redirect('orden:direccion')
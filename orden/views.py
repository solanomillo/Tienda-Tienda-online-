from django.shortcuts import get_object_or_404, redirect, render
from carts.funCart import deleteCart, funcionCarrito
from .utils import deleteOrden, funcionOrden, breadcrumb
from django.contrib.auth.decorators import login_required
from DirEnvio.models import DireccionEnvio
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorador import validar_cart_and_orden  


class OrdenView(LoginRequiredMixin, ListView):
    login_url = 'web:login'
    template_name = 'ordenes_historial.html'
    context_object_name = 'ordenes'  

    def get_queryset(self):
        return self.request.user.ordenes_completadas()




@login_required(login_url='web:login')
@validar_cart_and_orden
def orden(request,cart, orden):
        
    return render(request, 'orden.html', {
        'orden':orden,
        'cart': cart,
        'breadcrumb': breadcrumb(products=True),
    })



@login_required(login_url='web:login')
@validar_cart_and_orden
def direccion(request, cart, orden):
        
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
@validar_cart_and_orden
def check_direccion(request, cart, orden, pk):
    
    direccion_envio = get_object_or_404(DireccionEnvio, pk=pk)
    
    # Seguridad: Asegurar que la dirección le pertenece al usuario
    if direccion_envio.user != request.user:
        messages.warning(request, "No tienes permiso para usar esta dirección.")
        return redirect('web:index')
    
    orden.update_direccion_envio(direccion_envio)
    
    return redirect('orden:direccion')


@login_required(login_url='web:login')
@validar_cart_and_orden
def confirmacion(request,cart, orden):   
    
    direccion_envio = orden.direccion_envio
    
    if direccion_envio is None:
        return redirect('orden:direccion')
    
    return render(request, 'confirmacion.html', {
        'cart': cart,
        'orden': orden,
        'direccion_envio': direccion_envio,
        'breadcrumb':breadcrumb(address=True, confirmation=True)
    })
    
    
@login_required(login_url='web:login')
@validar_cart_and_orden
def cancelar_orden(request, cart, orden):    
    
    # Validación de seguridad: asegurar que la orden pertenece al usuario autenticado
    if orden.user != request.user:
        messages.error(request, "No tienes permiso para cancelar esta orden.")
        return redirect('web:index')


    orden.cancelar()    
    deleteCart(request)
    deleteOrden(request)
    messages.success(request, "Orden cancelada exitosamente.")
    # Redirige a la página de inicio o a donde desees después de cancelar la orden
    return redirect('web:index')


@login_required(login_url='web:login')
@validar_cart_and_orden
def completado(request, cart, orden):    
    
    # Validación de seguridad: asegurar que la orden pertenece al usuario autenticado
    if orden.user != request.user:
        messages.error(request, "No tienes permiso para completar esta orden.")
        return redirect('web:index')
    
    orden.completado()
    deleteCart(request)
    deleteOrden(request)
    messages.success(request, 'Compra realizada con éxito. Pronto llegará a tu dirección.')
    return redirect('web:index')
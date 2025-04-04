from django.shortcuts import render
from carts.funCart import funcionCarrito
from .utils import funcionOrden, breadcrumb
from django.contrib.auth.decorators import login_required

@login_required(login_url='web:login')
def orden(request):
    cart = funcionCarrito(request)
    orden = funcionOrden(cart, request)
        
    return render(request, 'orden.html', {
        'orden':orden,
        'cart': cart,
        'breadcrumb': breadcrumb,
    })

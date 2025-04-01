from django.shortcuts import render
from carts.funCart import funcionCarrito
from .utils import funcionOrden

def orden(request):
    cart = funcionCarrito(request)
    orden = funcionOrden(cart, request)
        
    return render(request, 'orden.html', {
        'orden':orden,
        'cart': cart        
    })

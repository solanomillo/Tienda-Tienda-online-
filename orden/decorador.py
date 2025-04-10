from .utils import funcionOrden
from carts.funCart import funcionCarrito

def validar_cart_and_orden(function):
    def wrap(request, *args, **kwargs):
        
        cart = funcionCarrito(request)
        orden = funcionOrden(cart, request)
        
        return function(request, cart, orden, *args, **kwargs)
    return wrap
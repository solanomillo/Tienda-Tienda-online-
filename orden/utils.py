from orden.models import Orden
from django.urls import reverse

def funcionOrden(cart, request):    
    orden = cart.orden
    
    if orden is None and request.user.is_authenticated:
        orden = Orden.objects.create(cart=cart, user=request.user)
    
    elif orden:
        request.session['orden_id'] = orden.id
        
    return orden


def breadcrumb(products=True, address=False, pyment=False, confirmation=False):
    return [
        {'title':'Productos', 'active':products, 'url':reverse('orden:orden')},
        {'title':'Dirección', 'active':address, 'url':reverse('orden:direccion')},
        {'title':'Pago', 'active':pyment, 'url':reverse('orden:orden')},
        {'title':'Confirmación', 'active':confirmation, 'url':reverse('orden:orden')},
    ]
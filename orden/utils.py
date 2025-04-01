from orden.models import Orden


def funcionOrden(cart, request):    
    orden = Orden.objects.filter(cart=cart).first()
    
    if orden is None and request.user.is_authenticated:
        orden = Orden.objects.create(cart=cart, user=request.user)
    
    elif orden:
        request.session['orden_id'] = orden.id
        
    return orden
    
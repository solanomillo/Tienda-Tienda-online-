from .models import Cart

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(usuario=request.user).first()
    else:
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.filter(cart_id=cart_id).first() if cart_id else None
    return {'cart': cart}
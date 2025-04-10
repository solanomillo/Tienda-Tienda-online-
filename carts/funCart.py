from pyexpat.errors import messages
from carts.models import Cart


def funcionCarrito(request):
    try:
        user = request.user if request.user.is_authenticated else None
        cart_id = request.session.get('cart_id')

        # Para usuarios logueados: buscar carrito asociado al usuario
        if user:
            cart = Cart.objects.filter(usuario=user).first()
            if cart:
                # Si había un cart_id en sesión diferente, actualizarlo
                if cart_id and str(cart.cart_id) != cart_id:
                    request.session['cart_id'] = str(cart.cart_id)
                return cart
        
        # Para usuarios anónimos o logueados sin carrito
        if cart_id:
            cart = Cart.objects.filter(cart_id=cart_id).first()
            if cart:
                if user and not cart.usuario:
                    cart.usuario = user
                    cart.save()
                return cart
        
        # Crear nuevo carrito si no existe
        cart = Cart.objects.create(usuario=user)
        request.session['cart_id'] = str(cart.cart_id)
        return cart
    
    except Exception as e:
        messages.error(request, "Ocurrió un error con el carrito")
        print(f"Error en carrito: {e}")
        # Crear carrito de emergencia
        cart = Cart.objects.create()
        request.session['cart_id'] = str(cart.cart_id)
        return cart


def deleteCart(request):
    request.session['cart_id'] = None

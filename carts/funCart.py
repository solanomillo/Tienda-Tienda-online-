from django.shortcuts import redirect
from carts.models import Cart
from django.contrib import messages

def funcionCarrito(request):
    try:
        # Obtén el usuario si está autenticado, de lo contrario None
        user = request.user if request.user.is_authenticated else None
        cart_id = request.session.get('cart_id')

        # Obtén el carrito de la base de datos usando el cart_id
        cart = Cart.objects.filter(cart_id=cart_id).first()

        # Si no existe el carrito, crea uno nuevo asociado al usuario
        if cart is None:
            cart = Cart.objects.create(usuario=user)
        
        # Si el carrito existe pero no está asociado a un usuario, asócialo
        elif user and cart.usuario is None:
            cart.usuario = user
            cart.save()

        # Asegúrate de que el cart_id esté en la sesión
        request.session['cart_id'] = str(cart.cart_id)

        return cart
    
    except Exception as e:
        # Mostrar mensaje de error al usuario
        messages.error(request, "Ocurrió un error con el carrito. Por favor, intente nuevamente.")
        print(f"Error en carrito: {e}")
        return redirect('/')  # Redirige a la página principal

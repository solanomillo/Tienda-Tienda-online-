from django.shortcuts import redirect, render, get_object_or_404
from carts.models import CartProduct
from web.models import Producto
from .funCart import funcionCarrito
from django.contrib import messages

# Create your views here.
def cart(request):
    cart = funcionCarrito(request)    
    return render(request, 'carts/cart.html', {'cart': cart})



def agregarCarrito(request, producto_id):
    # Obtener o crear el carrito
    cart = funcionCarrito(request)

    # Obtener el producto o devolver un error 404 si no existe
    producto = get_object_or_404(Producto, pk=producto_id)

    # Obtener la cantidad desde el formulario (si existe), por defecto 1
    cantidad = int(request.POST.get('cantidad', 1))    
    
    
    # Agregar el producto al carrito y la cantidad 
    #cart.producto.add(producto, through_defaults={
        #'cantidad':cantidad
    #})
    CartProduct.objects.creaActualizar(cart=cart, producto=producto, cantidad=cantidad)

    # Mostrar mensaje de éxito
    messages.success(request, f"✅ {producto.titulo} agregado al carrito.")

    # Redirigir a la página de carrito o a la página de productos
    return redirect(request.META.get('HTTP_REFERER', '/'))




from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from carts.models import CartProduct

def eliminarProductoCarrito(request, slug):
    cart = funcionCarrito(request)
    producto = get_object_or_404(Producto, slug=slug)
    
    try:
        cart_product = CartProduct.objects.get(cart=cart, producto=producto)
        cart_product.delete()
        cart.update_totals()  
        
        messages.success(request, f"🗑️ {producto.titulo} eliminado")
        
        # Redirige a la misma página desde donde vino
        if 'carrito' in request.META.get('HTTP_REFERER', ''):
            return redirect('cart:carrito')
        return redirect(request.META.get('HTTP_REFERER', 'web:index'))
        
    except CartProduct.DoesNotExist:
        messages.error(request, "⚠️ Producto no encontrado en el carrito")
        return redirect('web:index')

def vaciarCarrito(request):  
    cart = funcionCarrito(request)
    cart.cartproduct_set.all().delete()  # Elimina todos los productos
    cart.subtotal = 0
    cart.total = 0
    cart.save()
    
    # Para usuarios anónimos
    if not request.user.is_authenticated:
        if 'cart_id' in request.session:
            del request.session['cart_id']
        cart.delete()
    
    return redirect('cart:carrito')


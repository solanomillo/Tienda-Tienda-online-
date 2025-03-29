from django.shortcuts import redirect, render, get_object_or_404
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
    cart.producto.add(producto, through_defaults={
        'cantidad':cantidad
    })

    # Mostrar mensaje de éxito
    messages.success(request, f"✅ {producto.titulo} agregado al carrito.")

    # Redirigir a la página de carrito o a la página de productos
    return redirect(request.META.get('HTTP_REFERER', '/'))


def eliminarProductoCarrito(request,slug):
    from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def eliminarProductoCarrito(request, slug):
    try:
        # Obtener el carrito
        cart = funcionCarrito(request)
        
        # Obtener el producto (usando get_object_or_404 para manejo de errores)
        producto = get_object_or_404(Producto, slug=slug)
        
        # Verificar si el producto está en el carrito antes de eliminarlo
        if cart.producto.filter(slug=slug).exists():
            cart.producto.remove(producto)
            messages.success(request, f"✅ {producto.titulo} eliminado del carrito")
        else:
            messages.warning(request, f"⚠️ El producto {producto.titulo} no estaba en tu carrito")
            
    except Exception as e:
        messages.error(request, "❌ Ocurrió un error al eliminar el producto")       
    
    # Redirigir a la vista del carrito (no a un template directamente)
    return redirect('cart:carrito')  # Asegúrate de usar el nombre de tu URL


from django.shortcuts import redirect
from django.contrib import messages

def vaciarCarrito(request):
    try:
        # Obtener el carrito actual
        cart = funcionCarrito(request)
        
        # Verificar si el carrito tiene productos antes de vaciarlo
        if cart.producto.exists():
            # Vaciar el carrito
            cart.producto.clear()          
            
    except Exception as e:
        # Registrar el error para debugging (opcional)        
        messages.error(request, "❌ Ocurrió un error al vaciar el carrito")
    
    # Redirigir a la vista del carrito
    return redirect('cart:carrito')
    


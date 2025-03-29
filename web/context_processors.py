from .models import Categoria
from carts.models import Cart

def categorias_disponibles(request):
    return {
        'categorias': Categoria.objects.all()
    }

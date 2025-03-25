from .models import Categoria

def categorias_disponibles(request):
    return {
        'categorias': Categoria.objects.all()
    }

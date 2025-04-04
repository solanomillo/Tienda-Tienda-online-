from django.shortcuts import redirect, render
from django.contrib.auth import login as lg
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from .forms import Registro
from django.contrib.auth.models import User
from .models import Categoria, Producto
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
# Create your views here.

""" Vistas para el Listado y Detalle del Producto """
class ProductoListView(ListView):
    template_name = 'index.html'
    queryset = Producto.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensaje'] = 'Productos'
        context['categorias'] = Categoria.objects.all()  # Agregar categorías al contexto
        return context


class ProductosPorCategoriaListView(ListView):
    template_name = 'index.html'
    context_object_name = 'producto_list'

    def get_queryset(self):
        slug = self.kwargs['slug']
        categoria = get_object_or_404(Categoria, slug=slug)
        return Producto.objects.filter(categoria=categoria)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['categoria_actual'] = get_object_or_404(Categoria, slug=self.kwargs['slug'])  
        return context



class ProductoDetalleView(DetailView):
    model = Producto
    template_name = 'productoDetalle.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
    
    
def userLogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        usuarios = authenticate(request, username=username, password=password)
        
        if usuarios is not None:
            lg(request, usuarios)
            messages.success(request, f'Bienvenido {usuarios.username}')
            
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next') )
                
            return redirect('/')
        else:
            messages.error(request, 'Datos incorrectos')
    return render(request, 'login.html',{})


def salir(request):
    logout(request)
    messages.success(request,'Sesión finalizada')
    return redirect('web:login')


def registro(request):
    if request.user.is_authenticated:
        return redirect('/')
    Dataform = Registro()    
    if request.method == 'POST':
        Dataform = Registro(request.POST or None)
        if Dataform.is_valid():
            data = Dataform.cleaned_data
            
            username = data['username']
            password = data['password']
            email = data['email']
            
            nuevoUsuario = User.objects.create_user(username=username, password=password, email=email)
            
            if nuevoUsuario is not None:
                lg(request, nuevoUsuario)
                messages.success(request,f'Bienvenido {username}')
                return redirect('web:index')        
            
        
    return render(request, 'registro.html',{
        'form': Dataform
    }) 
    
""" Vistas para la busqueda de Productos """
    
# Versión mejorada (manteniendo GET pero con nombres más descriptivos)
class BuscarProductoListView(ListView):
    template_name = 'busqueda.html'
    
    def get_queryset(self):
        # Usamos 'q' (query) en vez de 'i' que es más estándar
        query = self.request.GET.get('q', '').strip()
        if query:
            return Producto.objects.filter(titulo__icontains=query)
        return Producto.objects.none()  # No devuelve resultados si no hay query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context  
    
    


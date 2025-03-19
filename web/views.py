from django.shortcuts import redirect, render
from django.contrib.auth import login as lg
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from .forms import Registro
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'index.html', {
        'mensaje':'Tienda',
        'titulo': 'Inicio',
        'productos':[
            {'titulo':'Campera', 'precio':15, 'stock':False},
            {'titulo':'Pantalon', 'precio':24, 'stock':True},
            {'titulo':'Remera', 'precio':11, 'stock':False},
            {'titulo':'Gorra', 'precio':44, 'stock':True},
        ]
    })


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        usuarios = authenticate(request, username=username, password=password)
        
        if usuarios is not None:
            lg(request, usuarios)
            messages.success(request, f'Bienvenido {usuarios.username}')
            return redirect('index')
        else:
            messages.error(request, 'Datos incorrectos')
    return render(request, 'login.html',{})


def salir(request):
    logout(request)
    messages.success(request,'Sesión finalizada')
    return redirect('login')


def registro(request):
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
                return redirect('index')        
            
        
    return render(request, 'registro.html',{
        'form': Dataform
    }) 
from django.shortcuts import render
from .models import DireccionEnvio
from django.views.generic import ListView
from .forms import DireccionEnvioForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



class EnvioDirecciones(LoginRequiredMixin,ListView):
    login_url = 'web:login'
    model = DireccionEnvio
    template_name = 'direccion_envio.html'
    
    def get_queryset(self):
        return DireccionEnvio.objects.filter(user=self.request.user).order_by('-default') 

@login_required(login_url='web:login')
def FormularioDir(request):
    form = DireccionEnvioForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        direccion_envio = form.save(commit=False)
        direccion_envio.user = request.user
        direccion_envio.default = not DireccionEnvio.objects.filter(user=request.user).exists()
        direccion_envio.save()
        
        messages.success(request, 'Dirección creada correctamente')
        return redirect('Envio:direccion_envio')
        
    return render(request, 'formulario.html', {
        'form': form
    })
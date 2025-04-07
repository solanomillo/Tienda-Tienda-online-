from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import DireccionEnvio
from django.views.generic import ListView
from .forms import DireccionEnvioForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView


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


class UpdateDireccion(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'web:login'
    model = DireccionEnvio
    form_class = DireccionEnvioForm
    template_name = 'actualizar_form.html'
    success_message = 'Datos Actualizados Correctamente'
    
    def get_success_url(self):
        return reverse('Envio:direccion_envio')


class DeleteDireccion(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url= 'web:login'
    model = DireccionEnvio
    template_name = 'eliminar_dir.html'
    success_message = 'Dirección eliminada'
    success_url = reverse_lazy('Envio:direccion_envio')
    
    # protege los datos del usuario y evita accesos maliciosos.
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            messages.warning(request, "No puedes eliminar la dirección predeterminada.")
            return redirect('Envio:direccion_envio')
        
        elif request.user.id != self.get_object().user_id:
            return redirect('web:index')        
        
        return super(DeleteDireccion, self).dispatch(request, *args, **kwargs)
    


@login_required(login_url='web:login')
def funcDefault(request, pk):
    direccion_envio = get_object_or_404(
        DireccionEnvio.objects.select_related("user"), pk=pk, user=request.user
    )
    direccion_envio.set_as_default()
    return redirect('Envio:direccion_envio')
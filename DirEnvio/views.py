from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
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
from carts.funCart import funcionCarrito
from orden.utils import funcionOrden

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
        direccion_envio.default = not request.user.has_direccion_envio()
        direccion_envio.save()
        
        next_url = request.GET.get('next')

        # 2. Se verifica que "next_url" exista y sea una URL válida dentro del mismo dominio
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            
            # 3. Si la URL coincide con la vista de dirección de envío (ruta "orden:direccion")
            if next_url == reverse('orden:direccion'):
                
                # 4. Obtiene el carrito actual asociado al usuario (esto depende de tu lógica interna)
                cart = funcionCarrito(request)
                
                # 5. Obtiene o crea una orden asociada al carrito y usuario
                orden = funcionOrden(cart, request)
                
                # 6. Actualiza la dirección de envío en esa orden con la seleccionada por el usuario
                orden.update_direccion_envio(direccion_envio)
                
                # 7. Redirige al usuario a la URL que estaba almacenada en "next"
                return HttpResponseRedirect(next_url)
            
        messages.success(request, 'Dirección creada correctamente')
        return redirect('DirEnvio:direccion_envio')
        
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
        return reverse('DirEnvio:direccion_envio')


class DeleteDireccion(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url= 'web:login'
    model = DireccionEnvio
    template_name = 'eliminar_dir.html'
    success_message = 'Dirección eliminada'
    success_url = reverse_lazy('DirEnvio:direccion_envio')
    
    # protege los datos del usuario y evita accesos maliciosos.
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            messages.warning(request, "No puedes eliminar la dirección predeterminada.")
            return redirect('DirEnvio:direccion_envio')
        
        elif self.get_object().has_orden():
            messages.warning(request, "No puedes eliminar esta dirección porque está asociada a una orden.")
            return redirect('orden:direccion')
        
        elif request.user.id != self.get_object().user_id:
            return redirect('web:index')        
        
        return super(DeleteDireccion, self).dispatch(request, *args, **kwargs)
    


@login_required(login_url='web:login')
def funcDefault(request, pk):
    direccion_envio = get_object_or_404(
        DireccionEnvio.objects.select_related("user"), pk=pk, user=request.user
    )
    direccion_envio.set_as_default()
    return redirect('DirEnvio:direccion_envio')
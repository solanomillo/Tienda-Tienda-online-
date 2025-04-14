from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='web:login')
def metodo_pago(request):
    """Vista para el método de pago."""
    return render(request, 'metodo_pago.html')
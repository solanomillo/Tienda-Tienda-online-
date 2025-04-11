from django.shortcuts import render
from django.http import JsonResponse

from promo_codigo.models import PromoCodigo
from orden.decorador import validar_cart_and_orden


@validar_cart_and_orden
def validar(request, cart, orden):
    codigo = request.GET.get('codigo', None)
    promo_codigo = PromoCodigo.objects.get_validar(codigo)
    
    if promo_codigo is None:
            return JsonResponse({
                'status': False
            }, status=404)
    
    orden.aplicarCodigo(promo_codigo)   
        
    return JsonResponse({
            'status': True,
            'codigo': promo_codigo.codigo,
            'descuento': promo_codigo.descuento,
            'total':orden.total
        })

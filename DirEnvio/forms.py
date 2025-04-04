from django.forms import ModelForm
from .models import DireccionEnvio

class DireccionEnvioForm(ModelForm):
    class Meta:
        model = DireccionEnvio
        fields = [
            'ciudad', 'estado', 'pais','postal_codigo','linea1', 'reference'
        ]
        
        labels = {
            'linea1': 'Dirección',            
            'ciudad': 'Ciudad',
            'estado': 'Provincia',
            'pais': 'País',
            'postal_codigo': 'Código Postal',
            'reference': 'Referencia'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['linea1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder':'San lucas 144'
        })      
        
        
        self.fields['ciudad'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['estado'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['pais'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['postal_codigo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '7600'
        })
        self.fields['reference'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ej: Portón Blanco'
        })

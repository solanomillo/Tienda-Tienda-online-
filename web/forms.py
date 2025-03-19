from django import forms
from django.contrib.auth.models import User

class Registro(forms.Form):
    username = forms.CharField(label='Nombre',min_length=5, max_length=40, required=True,
                               widget=forms.TextInput(attrs={
                                       'class':'form-control',
                                       'placeholder': 'Nombre de usuario',
                                   }
                               ))
    email = forms.EmailField(label='E-mail',required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@gmail.com',
        }
    ))
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
    }))
    password2 = forms.CharField(label='Confirmar contraseña', required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }
    ))
    
    def clean_username(self):
        username = self.data['username']
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuario ya existente')
        
        return username
    
    def clean_email(self):
        email = self.data['email']
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Correo ya registrado')
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'La contraseña no coincide')
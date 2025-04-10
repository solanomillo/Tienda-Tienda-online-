from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from orden.opciones import OrdenStatus

class User(AbstractUser):
    def get_full_name(self):
        return f'{self.first_name}, {self.last_name}'

    @property
    def direccion_envio(self):
        # Usa select_related para optimizar la consulta si luego usas relaciones
        return self.direcciones.filter(default=True).select_related().first()

    def has_direccion_envio(self):
        return self.direccion_envio is not None
    
    
    def ordenes_completadas(self):
        return self.orden_set.filter(
            status=OrdenStatus.COMPLETED
        ).select_related('user').order_by('-fecha_registro')





class Categoria(models.Model):
    titulo = models.CharField(max_length=40) 
    slug = AutoSlugField(populate_from='titulo', null=False, blank=False, unique=True)  
    fechar_registro = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.titulo 

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    titulo = models.CharField(max_length=40)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    fecha_registro = models.DateField(auto_now_add=True)
    slug = AutoSlugField(populate_from='titulo', null=False, blank=False, unique=True)
    imagen = models.ImageField(upload_to='productos', blank=True)    
    
    
    def __str__(self):
        return self.titulo 

class Cliente(User):
    class Meta:
        proxy: True
        
    def get_products(self):
        return []
    
    
    
    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField()
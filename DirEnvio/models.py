from django.db import models
from web.models import User

class DireccionEnvio(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    linea1 = models.CharField(max_length=300)
    linea2 = models.CharField(max_length=300, blank=True)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    reference = models.CharField(max_length=300)
    postal_codigo = models.CharField(max_length=10, null=False, blank=False)
    default = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.postal_codigo

    @property
    def direccion(self):
        return f'{self.ciudad}-{self.estado}-{self.pais}'
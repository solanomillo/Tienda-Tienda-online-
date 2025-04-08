from django.db import models
from web.models import User


class DireccionEnvio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="direcciones")
    linea1 = models.CharField(max_length=300)
    linea2 = models.CharField(max_length=300, blank=True)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    reference = models.CharField(max_length=300)
    postal_codigo = models.CharField(max_length=10)
    default = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.linea1}, {self.ciudad}"

    @property
    def direccion(self):
        return f'{self.ciudad} - {self.estado}'

    def set_as_default(self):
        # Desactiva las demás direcciones en una sola query
        DireccionEnvio.objects.filter(user=self.user, default=True).update(default=False)
        self.default = True
        self.save(update_fields=["default"])
    
    def has_orden(self):
        return self.orden_set.exists()

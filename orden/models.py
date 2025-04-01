from django.db import models
from web.models import User
from carts.models import Cart
from enum import Enum
import uuid
from django.db.models.signals import pre_save

class OrdenStatus(Enum):
    CREATED = 'CREADO'
    PAYED = 'PAGADO'
    COMPLETED = 'COMPLETADO'
    CANCELED = 'CANCELADO'


choices = [(tag, tag.value) for tag in OrdenStatus]

class Orden(models.Model):
    ordenID = models.CharField(max_length=100, null=False, blank=False, unique= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=40, choices=choices, default=OrdenStatus.CREATED)
    envio_total = models.DecimalField(default=10 , max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.ordenID
    

def enviarOrden(sender, instance, *args, **kwargs):
    if not instance.ordenID:
        instance.ordenID = str(uuid.uuid4())

pre_save.connect(enviarOrden, sender=Orden)
    


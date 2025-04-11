from django.utils import timezone
import random
import string
from django.db import models
from django.db.models.signals import pre_save


class PromoCodigoManager(models.Manager):     
    def get_validar(self, codigo):
        actual = timezone.now()
        return self.filter(
            codigo=codigo,
            used=False,
            fecha_inicio__lte=actual,
            fecha_final__gte=actual
        ).first()




class PromoCodigo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.FloatField(default=0.0)
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    used = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    objects = PromoCodigoManager()
    
    def __str__(self):
        return self.codigo
    
    
    def codigo_usado(self):
        self.used = True
        self.save()

def set_codigo(sender, instance, *args, **kwargs):
    if instance.codigo:
        return
    
    coder = string.ascii_uppercase + string.digits
    instance.codigo = ''.join( random.choices(coder, k=5))
    
    
pre_save.connect(set_codigo, sender=PromoCodigo)
        
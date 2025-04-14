from django.db import models
from web.models import User

class ProfilePago(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_pago')
    token = models.CharField(max_length=50, null=False, blank=False)
    card_id = models.CharField(max_length=50, null=False, blank=False)
    last4 = models.CharField(max_length=4, null=False, blank=False)
    brand = models.CharField(max_length=10, null=False, blank=False)
    default = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.card_id

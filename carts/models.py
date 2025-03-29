from django.db import models
from web.models import User, Producto
import uuid
from django.db.models.signals import pre_save
import decimal
from django.db.models.signals import m2m_changed
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    usuario = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto, through='CartProduct')
    subtotal = models.DecimalField(decimal_places=2, default=0.0, max_digits=8)
    total = models.DecimalField(decimal_places=2, default=0.0, max_digits=8)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    FEE = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)

    
    def __str__(self):
        return self.cart_id

    def update_totals(self):
        self.update_subtotal()
        self.update_total()
    
    def update_subtotal(self):
        self.subtotal = sum([producto.precio for producto in self.producto.all()])
        self.save()
    
    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))
        self.save()
        
    def product_related(self):
        return self.cartproduct_set.select_related('producto')



class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    

def set_cart_id(sender, instance, *arg, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def update_totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()
        
pre_save.connect(set_cart_id, sender=Cart)
#m2m_changed.connect(update_totals, sender=Cart.producto.through)
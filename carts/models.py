from django.db import models
from web.models import User, Producto
import uuid
from django.db.models.signals import pre_save, post_save
import decimal
from django.db.models.signals import m2m_changed
from django.db.models import F
from django.contrib.sessions.backends.db import SessionStore  
from django.conf import settings  

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
        
        if self.orden:
            self.orden.update_total()
    
    def update_subtotal(self):
        subtotal = self.cartproduct_set.aggregate(
            subtotal=models.Sum(models.F("cantidad") * models.F("producto__precio"))
        )["subtotal"] or 0  # Si no hay productos, devuelve 0
        
        self.subtotal = decimal.Decimal(subtotal)  # Asegura que sea Decimal
        self.save()

    
    def update_total(self):
        subtotal = decimal.Decimal(self.subtotal or 0)  # Convierte subtotal a Decimal
        fee = self.FEE if isinstance(self.FEE, decimal.Decimal) else decimal.Decimal(str(self.FEE))  # Convierte FEE correctamente

        self.total = subtotal + (subtotal * fee)  # Aplica la comisión correctamente
        self.save()
    
    def get_total_quantity(self):
        return self.cartproduct_set.aggregate(total=models.Sum('cantidad'))['total'] or 0
            
                        

        
    def product_related(self):
        return self.cartproduct_set.select_related('producto').distinct()  # Evita duplicados


    @property
    def orden(self):
        return self.orden_set.first()
    
class CartProductManager(models.Manager): 
     
    def creaActualizar(self, cart, producto, cantidad=1):
        obj, created = self.get_or_create(cart=cart, producto=producto)
        
        if not created:
            # Actualizamos la cantidad sumando la nueva cantidad
            obj.cantidad += cantidad
            obj.save()  # Guardamos el objeto
        else:
            obj.cantidad = cantidad
            obj.save()  # Guardamos el nuevo objeto
        
        # Al final, actualizamos los totales del carrito
        cart.update_totals()
        
        return obj
    
    
    def restaActualizar(self, cart, producto, cantidad=1):
        obj, created = self.get_or_create(cart=cart, producto=producto)
        
        if not created:
            # Restar la cantidad, pero asegurándote de no dejarla en 0 o negativa
            new_quantity = obj.cantidad - cantidad
            if new_quantity > 0:  # Si la cantidad sigue siendo positiva, actualiza
                obj.cantidad = new_quantity
                obj.save()
            else:  # Si la cantidad es 0 o negativa, elimina el producto
                obj.delete()  # Elimina el producto del carrito
        else:
            obj.cantidad = cantidad
            obj.save()  # Si es nuevo, asigna la cantidad y guarda

        # Al final, actualiza los totales del carrito
        cart.update_totals()

        return obj


    



class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_registro = models.DateTimeField(auto_now_add=True)    
    objects = CartProductManager()  

    def update_quantity(self, cantidad):
        self.cantidad = cantidad
        self.save()
    

def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())        
        # Guardar cart_id en la sesión SOLO para usuarios no logueados
        if not instance.usuario:
            session = SessionStore()
            session['cart_id'] = instance.cart_id
            session.save()  # ¡IMPORTANTE! Guarda la sesión en la base de datos

def update_totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

def postActualizar(sender, instance, *args, **kwargs):
    instance.cart.update_totals()
    
post_save.connect(postActualizar, sender=CartProduct)      
pre_save.connect(set_cart_id, sender=Cart)
m2m_changed.connect(update_totals, sender=Cart.producto.through)
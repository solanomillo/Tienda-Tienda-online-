from django.contrib import admin
from .models import Cart, CartProduct

class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'fecha_registro')
    can_delete = False  # Opcional: evitar eliminaciones desde admin

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'usuario', 'subtotal', 'total', 'fecha_registro']
    inlines = [CartProductInline]

admin.site.register(Cart, CartAdmin)

from django.contrib import admin
from .models import Producto , Categoria

# Register your models here.
admin.site.register(Categoria)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'slug' , 'fecha_registro','categoria')
    list_editable = ('precio',)
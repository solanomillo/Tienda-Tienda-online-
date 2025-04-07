from django.contrib import admin
from .models import Producto , Categoria
from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Categoria)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'slug' , 'fecha_registro','categoria')
    list_editable = ('precio',)
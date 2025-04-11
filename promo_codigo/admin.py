from django.contrib import admin
from .models import PromoCodigo


@admin.register(PromoCodigo)
class PromoCodigoAdmin(admin.ModelAdmin):
    exclude = ['codigo']



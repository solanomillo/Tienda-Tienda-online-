from django import template

register = template.Library()

@register.filter(name='peso_argentino')
def peso_argentino(value):
    try:
        # Convierte el valor a float para manejar decimales
        value = float(value)
        # Formatea el número con puntos como separadores de miles y coma como separador decimal
        formatted_value = "{:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted_value
    except (ValueError, TypeError):
        # Si no se puede convertir a número, devuelve el valor original
        return value
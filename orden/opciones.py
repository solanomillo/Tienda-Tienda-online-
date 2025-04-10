
from enum import Enum

class OrdenStatus(Enum):
    CREATED = 'CREADO'
    PAYED = 'PAGADO'
    COMPLETED = 'COMPLETADO'
    CANCELED = 'CANCELADO'


choices = [(tag, tag.value) for tag in OrdenStatus]
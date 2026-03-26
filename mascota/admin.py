from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(EspecieMascota)
admin.site.register(RazaMascota)
admin.site.register(Mascota)
admin.site.register(HistorialMedicoMascota)
admin.site.register(EstadoMascota)
admin.site.register(UbicacionMascota)
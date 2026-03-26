from django.db import models
from usuario.models import Usuario
from fundacion.models import Fundacion
from django.core.exceptions import ValidationError

class Direccion(models.Model):
    usuario = models.ForeignKey(
        Usuario, null=True, blank=True, on_delete=models.CASCADE, related_name="direcciones_usuario"
    )
    fundacion = models.ForeignKey(
        Fundacion, null=True, blank=True, on_delete=models.CASCADE, related_name="direcciones_fundacion"
    )
    direccion_linea = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    referencia = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Al menos usuario o fundacion deben estar presentes
        if not self.usuario and not self.fundacion:
            raise ValidationError("Una dirección debe pertenecer a un usuario o a una fundación.")

    def __str__(self):
        return f"{self.direccion_linea}, {self.comuna}, {self.ciudad}, {self.region}"
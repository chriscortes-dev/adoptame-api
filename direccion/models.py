from django.db import models


class Direccion(models.Model):
    direccion_linea = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    referencia = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna}"
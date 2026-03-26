from django.db import models
from usuario.models import Usuario
from direccion.models import Direccion

class Fundacion(models.Model):
    nombre = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    direccion = models.ManyToManyField(
        Direccion,
        blank=True
    )

    miembros = models.ManyToManyField(
        Usuario,
        through='FundacionMiembro',
        related_name='fundaciones'
    )

    def __str__(self):
        return self.nombre


class FundacionMiembro(models.Model):
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('MIEMBRO', 'Miembro'),
    ]

    fundacion = models.ForeignKey(Fundacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='MIEMBRO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('fundacion', 'usuario')

    def __str__(self):
        return f'{self.usuario.username} ({self.rol}) en {self.fundacion.nombre}'
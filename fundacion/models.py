from django.db import models
from django.contrib.auth.models import User

class Fundacion(models.Model):
    nombre = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    miembros = models.ManyToManyField(
        User,
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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='MIEMBRO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('fundacion', 'usuario')

    def __str__(self):
        return f'{self.usuario.username} ({self.rol}) en {self.fundacion.nombre}'
from django.contrib.auth.models import AbstractUser
from django.db import models
from direccion.models import Direccion

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)

    # Relación a direcciones (puede ser null al inicio)
    direccion = models.ForeignKey(
        Direccion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Para evitar conflictos con grupos y permisos
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuario_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuario_permissions",
        blank=True
    )

    # Timestamp de última actualización
    updated_at = models.DateTimeField(auto_now=True)

    # Campos obligatorios para crear usuario
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
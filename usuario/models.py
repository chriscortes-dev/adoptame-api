from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    direcciones = models.ManyToManyField(
        "direcciones.Direccion",
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

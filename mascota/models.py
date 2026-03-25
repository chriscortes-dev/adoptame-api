from django.db import models
from fundacion.models import Fundacion
from direccion.models import Direccion
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class EspecieMascota(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class RazaMascota(models.Model):
    especie = models.ForeignKey(EspecieMascota, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Mascota(models.Model):

    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]

    ACTIVIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    ]

    raza = models.ForeignKey(RazaMascota, on_delete=models.CASCADE)
    microchip = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    color = models.CharField(max_length=50)
    patron_color = models.CharField(max_length=50)

    sociable = models.BooleanField(default=False)
    actividad = models.CharField(max_length=10, choices=ACTIVIDAD_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
class HistorialMedicoMascota(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    esterilizado = models.BooleanField(default=False)
    tratamiento = models.BooleanField(default=False)
    observacion_tratamiento = models.TextField()
    vacunas = models.BooleanField(default=False)
    observacion_vacuna = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Historial de {self.mascota.nombre}'

class EstadoMascota(models.Model):

    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('ADOPTADO', 'Adoptado'),
        ('EN_REVISION', 'En revisión'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='estados')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.mascota} - {self.estado}'
    
class UbicacionMascota(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='ubicaciones')
    fundacion = models.ForeignKey(Fundacion, null=True, blank=True, on_delete=models.SET_NULL)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    direccion = models.ForeignKey(Direccion, on_delete=models.PROTECT)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            # Solo una ubicación activa por mascota
            models.UniqueConstraint(
                fields=['mascota'],
                condition=models.Q(fecha_fin__isnull=True),
                name='unique_active_ubicacion_por_mascota'
            )
        ]

    def clean(self):
        super().clean()

        # Regla 1: Exclusividad (usuario XOR fundacion)
        if bool(self.usuario) == bool(self.fundacion):
            raise ValidationError(
                "Debe existir solo usuario o fundacion, no ambos ni ninguno."
            )

        # Regla 2: Solo una ubicación activa por mascota
        if self.fecha_fin is None:
            if UbicacionMascota.objects.filter(
                mascota=self.mascota,
                fecha_fin__isnull=True
            ).exclude(pk=self.pk).exists():
                raise ValidationError(
                    "Esta mascota ya tiene una ubicación activa."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        target = self.fundacion or self.usuario or "Sin asignar"
        return f'{self.mascota.nombre} - {target}'
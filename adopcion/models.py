from django.db import models
from mascota.models import Mascota
from django.contrib.auth.models import User
from django.utils import timezone

class Adopcion(models.Model):

    CHOICES_ESTADO = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('DEVUELTA', 'Devuelta'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    #Motivo por el cual el usuario desea adoptar la mascota
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=CHOICES_ESTADO, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['mascota'],
                condition=models.Q(estado='APROBADO'),
                name='unique_active_adopcion_por_mascota'
            )
        ]

    def save(self, *args, **kwargs):
        # Validar adopción aprobada
        if self.estado == 'APROBADO':
            if Adopcion.objects.filter(mascota=self.mascota, estado='APROBADO').exclude(pk=self.pk).exists():
                raise ValueError("Esta mascota ya tiene una adopción aprobada.")

        # Registrar fecha de finalización automáticamente
        if self.estado in ['APROBADO', 'RECHAZADO', 'DEVUELTA'] and not self.fecha_finalizacion:
            self.fecha_finalizacion = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Adopción de {self.mascota.nombre} por {self.usuario.username} - Estado: {self.estado}'


class HistorialAdopcion(models.Model):
    adopcion = models.ForeignKey(Adopcion, on_delete=models.CASCADE, related_name='historial')
    #Observación de parte de la fundación al aprobar o rechazar la adopción
    comentario = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.adopcion.mascota.nombre} - {self.adopcion.estado} - {self.created_at:%Y-%m-%d %H:%M}'
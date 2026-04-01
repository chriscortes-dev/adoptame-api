from rest_framework import serializers
from .models import Mascota
from datetime import date

class MascotasDisponiblesSerializer(serializers.ModelSerializer):
    """
    Serializer para usuarios externos.
    
    Expone solo información necesaria para adopción:
    - Datos básicos de la mascota
    - Edad (derivada)
    - Historial médico resumido
    - Ubicación general (NO dirección exacta)
    """

    edad = serializers.SerializerMethodField()
    nombre_especie = serializers.CharField(source='raza.especie.nombre')
    nombre_raza = serializers.CharField(source='raza.nombre')

    class Meta:
        model = Mascota
        fields = [
            'id',
            'nombre_especie',
            'nombre_raza',
            'nombre',
            'edad',
            'sexo',
            'color',
            'patron_color',
            'sociable',
            'actividad',
        ]

    def get_edad(self, obj):
        hoy = date.today()
        nacimiento = obj.fecha_nacimiento

        edad = hoy.year - nacimiento.year

        if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
            edad -= 1

        return edad
    
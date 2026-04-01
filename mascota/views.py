from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import MascotasDisponiblesSerializer
from .models import Mascota

class MascotasDisponiblesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint público:
    Retorna solo mascotas cuyo estado actual es DISPONIBLE.
    """
    queryset = Mascota.objects.filter(estadomascota__estado='Disponible')
    serializer_class = MascotasDisponiblesSerializer
    permission_classes = [AllowAny]

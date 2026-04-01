from rest_framework import routers
from mascota.views import MascotasDisponiblesViewSet
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'mascotas/disponibles', MascotasDisponiblesViewSet, basename='mascotas-disponibles')

urlpatterns = [
    path('', include(router.urls)),
]
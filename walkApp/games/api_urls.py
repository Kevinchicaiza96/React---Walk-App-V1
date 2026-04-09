# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter
from .api_views import EstadisticasViewSet, HistoriaViewSet, MapaRotoViewSet

router = DefaultRouter()
router.register(r'estadisticas', EstadisticasViewSet, basename='estadisticas')
router.register(r'historial',    HistoriaViewSet,     basename='historial')
router.register(r'mapa-roto', MapaRotoViewSet, basename='mapa-roto')


urlpatterns = router.urls
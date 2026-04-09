# -*- coding: utf-8 -*-
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import HistorialJuegoTrivia, EstadisticasUsuarioTrivia, HistorialMapaRoto
from .serializers import HistoriaSerializer, EstadisticasSerializer, MapaRotoSerializer


class HistoriaViewSet(viewsets.ModelViewSet):
    serializer_class = HistoriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistorialJuegoTrivia.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha_juego')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class EstadisticasViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EstadisticasSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EstadisticasUsuarioTrivia.objects.filter(
            usuario=self.request.user
        )

    @action(detail=False, methods=['get'])
    def mias(self, request):
        """GET /api/juegos/estadisticas/mias/"""
        estadisticas, _ = EstadisticasUsuarioTrivia.objects.get_or_create(
            usuario=request.user
        )
        serializer = self.get_serializer(estadisticas)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        """GET /api/juegos/estadisticas/resumen/ — formato para Juegos.jsx"""
        estadisticas, _ = EstadisticasUsuarioTrivia.objects.get_or_create(
            usuario=request.user
        )
        ultimos = HistorialJuegoTrivia.objects.filter(
            usuario=request.user
        ).order_by('-fecha_juego')[:10]

        ultimos_data = [
            {
                'id':           j.id,
                'categoria':    j.get_categoria_display(),
                'categoria_key': j.categoria,
                'puntos':       j.puntos,
                'fecha':        j.fecha_juego.strftime('%d/%m/%Y'),
            }
            for j in ultimos
        ]

        return Response({
            'estadisticas': {
                'total_juegos':  estadisticas.total_juegos,
                'mejor_puntaje': estadisticas.mejor_puntaje,
                'tasa_acierto':  estadisticas.tasa_acierto_global,
            },
            'ultimos_juegos': ultimos_data,
        })


class MapaRotoViewSet(viewsets.ModelViewSet):
    serializer_class = MapaRotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistorialMapaRoto.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha_juego')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)